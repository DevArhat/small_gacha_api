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
            "pickup_5": 0,
            "other_5": 0,
            "star_4": 0,
            "weapon_3": 0,
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


def arrange_stats(stats: dict, change_rate: int = 20) -> dict:
    stats['total_pulls'] = stats['raw']['pulls']
    COST_PER_TRUCK = 119000
    PULLS_PER_TRUCK = 50.5
    COST_PER_PULL = COST_PER_TRUCK / PULLS_PER_TRUCK
    
    payback_tickets = stats['crumbs']['total'] // change_rate
    
    stats['raw']['cost'] = math.ceil(stats['raw']['pulls'] * COST_PER_PULL)
            
    stats['after_exchange']['pulls'] = max(1, stats['raw']['pulls'] - payback_tickets)
    stats['after_exchange']['cost'] = math.ceil(stats['after_exchange']['pulls'] * COST_PER_PULL)
    
    stats['trucks']['raw'] = math.ceil(stats['raw']['pulls'] / PULLS_PER_TRUCK)
    stats['trucks']['after_exchange'] = math.ceil(stats['after_exchange']['pulls'] / PULLS_PER_TRUCK)
    stats['trucks']['raw_cost'] = stats['trucks']['raw'] * COST_PER_TRUCK
    stats['trucks']['after_exchange_cost'] = stats['trucks']['after_exchange'] * COST_PER_TRUCK
    
    stats['crumbs']['tickets_changed'] = payback_tickets
    stats['crumbs']['remaining'] = stats['crumbs']['total'] % change_rate

    return stats