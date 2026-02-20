from fastapi import APIRouter
from typing import Optional

from models import SimulationResponse, Gacha
from simulator import GachaSimulator
from simulator.statistics import v2_get_gacha_statistics

# SpringBoot의 @RequestMapping("/v2")와 유사한 역할
router = APIRouter(prefix="/v2")
gacha = GachaSimulator()


@router.get("/statistics")
def get_statistics(game: str = 'all', target_rank: Optional[int] = None):
    result = v2_get_gacha_statistics(game, target_rank)
    return result


@router.get("/simulate", response_model=SimulationResponse)
def simulate_gacha(game: str = 'hsr', target_rank: int = 0):
    result = gacha.v2_simulate(game, target_rank)
    return result

@router.get("/simulate/{game}/{target_rank}", response_model=SimulationResponse)
def simulate_gacha_get(game: str, target_rank: int):
    result = gacha.v2_simulate(game, target_rank)
    return result

@router.post("/simulate/", response_model=SimulationResponse)
def simulate_gacha_post(gacha_request: Gacha):
    result = gacha.v2_simulate(gacha_request.game, gacha_request.target_rank)
    return result