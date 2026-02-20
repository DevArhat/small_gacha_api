from pydantic import BaseModel

class PullResult(BaseModel):
    pickup_6: int = 0 
    other_6: int = 0
    
    pickup_5: int = 0
    other_5: int = 0

    star_5: int = 0
    
    star_4: int = 0
    
    weapon_3: int = 0

class SimulationResponse(BaseModel):
    game: str
    target_rank: int
    total_pulls: int
    raw: dict
    after_exchange: dict
    trucks: dict
    pull_result: PullResult
    crumbs: dict
    logs: dict

class Gacha(BaseModel):
    game: str
    target_rank: int