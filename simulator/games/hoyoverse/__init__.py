import math

def arrange_stats(stats: dict, change_rate: int = 20) -> dict:
    stats['total_pulls'] = stats['raw']['pulls']
    COST_PER_TRUCK = 119000
    PULLS_PER_TRUCK = 50.5
    COST_PER_PULL = COST_PER_TRUCK / PULLS_PER_TRUCK
    
    payback_tickets = stats['crumbs']['total'] // change_rate
    
    stats['raw']['cost'] = math.ceil(stats['raw']['pulls'] * COST_PER_PULL)
            
    stats['after_exchange']['pulls'] = stats['raw']['pulls'] - payback_tickets
    stats['after_exchange']['cost'] = math.ceil(stats['after_exchange']['pulls'] * COST_PER_PULL)
    
    stats['trucks']['raw'] = math.ceil(stats['raw']['pulls'] / PULLS_PER_TRUCK)
    stats['trucks']['after_exchange'] = math.ceil(stats['after_exchange']['pulls'] / PULLS_PER_TRUCK)
    stats['trucks']['raw_cost'] = stats['trucks']['raw'] * COST_PER_TRUCK
    stats['trucks']['after_exchange_cost'] = stats['trucks']['after_exchange'] * COST_PER_TRUCK
    
    stats['crumbs']['tickets_changed'] = payback_tickets
    stats['crumbs']['remaining'] = stats['crumbs']['total'] % change_rate

    return stats