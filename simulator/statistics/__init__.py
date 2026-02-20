import json
from pathlib import Path
from typing import Optional

_base_dir = Path(__file__).resolve().parent


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def arrange_statistics(statistics: dict, game: str = 'all', target_rank: Optional[int] = None) -> dict:
    game_name = str(game).lower() if game else 'all'
    game_key = 'all'
    
    if game_name != 'all':
        if game_name in ['gen', 'genshin', 'genshinimpact']:
            game_key = 'gen'
        elif game_name in ['zzz', 'zen', 'zenless', 'zenzero', 'zenlesszonezero', 'zenzonezero']:
            game_key = 'zzz'
        elif game_name in ['wuwa', 'wutheringwaves']:
            game_key = 'wuwa'
        elif game_name in ['end', 'endfield']:
            game_key = 'end'
        else:
            game_key = 'hsr'
            
    if game_key != 'all' and target_rank is not None:
        rank_str = str(target_rank)
        return statistics.get(game_key, {}).get(rank_str, {})
        
    elif game_key != 'all' and target_rank is None:
        return statistics.get(game_key, {})
        
    elif game_key == 'all' and target_rank is not None:
        rank_str = str(target_rank)
        result = {}
        for g_key, g_data in statistics.items():
            if rank_str in g_data:
                result[g_key] = g_data[rank_str]
        return result
        
    else:
        return statistics
    

def get_gacha_statistics(game: str = 'all', target_rank: Optional[int] = None) -> dict:
    file_path = _base_dir / 'statistics.json'
    STATISTICS = load_json(file_path)
    
    return arrange_statistics(STATISTICS, game, target_rank)
    
def v2_get_gacha_statistics(game: str = 'all', target_rank: Optional[int] = None) -> dict:
    file_path = _base_dir / 'statistics_v2.json'
    STATISTICS = load_json(file_path)
    
    return arrange_statistics(STATISTICS, game, target_rank)
    

__all__ = ['get_gacha_statistics', 'v2_get_gacha_statistics']