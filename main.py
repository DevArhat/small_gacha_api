from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from simulator import GachaSimulator
import simulator.games
from simulator.statistics import get_gacha_statistics
from typing import Optional

app = FastAPI()
gacha = GachaSimulator()

class Gacha(BaseModel):
    game: str
    target_rank: int
    

@app.get("/")
def read_root():
    return {
        "title": "Gacha Simulator API",
        "description": "원신, 붕괴스타레일, 젠레스 존 제로, 명조, 엔드필드 가챠 시뮬레이터 API",
        "usage": "자세한 사용법은 github README 또는 /docs를 참고하세요.",
        "links": {
            "documentation": "/docs",
            "github": "https://github.com/DevArhat/small_gacha_api"
        },
    }

@app.get("/list")
def get_games_list_json():
    games_data = []
    for display_name, (_, aliases) in simulator.games.GAMES_CONFIG.items():
        games_data.append({
            "name": display_name,
            "aliases": aliases,
            "id": aliases[0] # 대표 ID로 첫 번째 별칭 사용
        })
    return {"games": games_data}

@app.get("/list/aliases")
def get_games_list():
    keys = simulator.games.GAMES_CONFIG.keys()
    values = [simulator.games.GAMES_CONFIG[key][1] for key in keys]
    return {"games": dict(zip(keys, values))}

@app.get("/statistics")
def get_statistics(game: str = 'all', target_rank: Optional[int] = None):
    result = get_gacha_statistics(game, target_rank)
    return result



@app.get("/simulate")
def simulate_gacha(game: str = 'hsr', target_rank: int = 0):
    result = gacha.simulate(game, target_rank)
    return result

@app.get("/simulate/{game}/{target_rank}")
def simulate_gacha_get(game: str, target_rank: int):
    result = gacha.simulate(game, target_rank)
    return result

@app.post("/simulate/")
def simulate_gacha_post(gacha_request: Gacha):
    result = gacha.simulate(gacha_request.game, gacha_request.target_rank)
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)