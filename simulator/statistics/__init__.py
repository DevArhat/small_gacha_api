import json
from pathlib import Path
from typing import Optional

_base_dir = Path(__file__).resolve().parent
_file_path = _base_dir / 'statistics.json'

with open(_file_path, 'r', encoding='utf-8') as file:
    STATISTICS = json.load(file)
    
def get_gacha_statistics(game: str = 'all', target_rank: Optional[int] = None) -> dict:
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
        return STATISTICS.get(game_key, {}).get(rank_str, {})
        
    elif game_key != 'all' and target_rank is None:
        return STATISTICS.get(game_key, {})
        
    elif game_key == 'all' and target_rank is not None:
        rank_str = str(target_rank)
        result = {}
        for g_key, g_data in STATISTICS.items():
            if rank_str in g_data:
                result[g_key] = g_data[rank_str]
        return result
        
    else:
        return STATISTICS

__all__ = ['STATISTICS', 'get_gacha_statistics']