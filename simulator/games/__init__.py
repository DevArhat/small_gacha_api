from .hoyo import HoyoverseGames
from .wuwa import WutheringWaves
from .arknights import Arknights
from .endfield import Endfield

# 게임 이름과 클래스를 매핑
GAME_MAP = {
    "mihoyo": HoyoverseGames,
    "wuwa": WutheringWaves,
    "arknights": Arknights,
    "endfield": Endfield
}

def get_game_strategy(game_name: str):
    game_name = game_name.lower()
    return GAME_MAP.get(game_name, "mihoyo")()