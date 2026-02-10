from simulator.games.hoyoverse.genshin import GenshinImpact
from simulator.games.hoyoverse.starrail import HonkaiStarRail
from simulator.games.hoyoverse.zenless import ZenlessZoneZero
from simulator.games.kurogames.wuwa import WutheringWaves
from simulator.games.hypergryph.arknights import Arknights
from simulator.games.hypergryph.endfield import Endfield


GAMES_CONFIG = {
    "원신": (GenshinImpact, ["gen", "genshin", "genshinimpact"]),
    "붕괴: 스타레일": (HonkaiStarRail, ["hsr", "honkaisr", "honkaistarrail"]),
    "젠레스 존 제로": (ZenlessZoneZero, ["zzz", "zen", "zenless", "zenzero"]),
    "명조": (WutheringWaves, ["wuwa", "wutheringwaves"]),
    # "명일방주": (Arknights, ["ark", "arknights"]),
    "엔드필드": (Endfield, ["end", "endfield"]),
}

ALIAS_MAP = {}

for display_name, (game_class, aliases) in GAMES_CONFIG.items():
    for alias in aliases:
        ALIAS_MAP[alias.lower()] = (game_class, display_name)

def get_game_strategy(input_name: str):
    key = input_name.lower()
    if key in ALIAS_MAP:
        game_class, display_name = ALIAS_MAP[key]
        return game_class(game_name=display_name)
    
    default_class, default_name = ALIAS_MAP["hsr"]
    return default_class(game_name=default_name)
    