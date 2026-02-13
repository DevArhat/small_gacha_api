import math
import copy

_STATS = {"game": "",
        "target_rank": 0,
        "total_pulls": 0,
        "raw":{
            "pulls":0,
            "cost":0,
            },
        "after_exchange":{
            "pulls":0,
            "cost":0,
            },
        "trucks":{
            "raw": 0,
            "after_exchange": 0,
            "raw_cost": 0,
            "after_exchange_cost": 0,
            },
        "pull_result":{
            "pickup_6": 0,
            "other_6": 0,
            "star_5": 0,
            "star_4": 0,
            },
        "crumbs": {
            "total": 0,
            "tickets_changed": 0,
            "remaining": 0,
            },
        "logs": {
            "log": [],
            "target": [] 
            }
        }


def init_stats() -> dict:
    return copy.deepcopy(_STATS)


def end_arrange_stats(stats: dict) -> dict:
    stats['total_pulls'] = stats['raw']['pulls']
    COST_PER_TRUCK = 153000
    PULLS_PER_TRUCK = 60
    COST_PER_PULL = COST_PER_TRUCK / PULLS_PER_TRUCK
    CRUMBS_PER_WEAPON_PULL = 198
    
    weapon_tickets = stats['crumbs']['total'] // CRUMBS_PER_WEAPON_PULL
    
    stats['raw']['cost'] = math.ceil(stats['raw']['pulls'] * COST_PER_PULL)
            
    stats['after_exchange']['pulls'] = 0
    stats['after_exchange']['cost'] = 0
    
    stats['trucks']['raw'] = math.ceil(stats['raw']['pulls'] / PULLS_PER_TRUCK)
    stats['trucks']['after_exchange'] = math.ceil(stats['after_exchange']['pulls'] / PULLS_PER_TRUCK)
    stats['trucks']['raw_cost'] = stats['trucks']['raw'] * COST_PER_TRUCK
    stats['trucks']['after_exchange_cost'] = stats['trucks']['after_exchange'] * COST_PER_TRUCK
    
    stats['crumbs']['tickets_changed'] = weapon_tickets
    stats['crumbs']['remaining'] = stats['crumbs']['total'] % CRUMBS_PER_WEAPON_PULL

    return stats

def ark_arrange_stats(stats: dict) -> dict:
    return stats