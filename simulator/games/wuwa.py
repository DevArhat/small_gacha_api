import random
from ._base import Game

class WutheringWaves(Game):
    def run_simulation(self, target_rank):
        # 명조: 0.8% / 66회 soft pity / 80회 hard pity / 4성 10회 천장
        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                 "total_pulls": 0,
                 "pickup_5": 0,
                 "other_5": 0,
                 "4_star": 0,
                 "log":[]}
        
        pity_5 = 0
        pity_4 = 0
        guaranteed = False
        
        while stats["pickup_5"] < target_copies:
            stats["total_pulls"] += 1
            pity_5 += 1
            pity_4 += 1
            
            rate_5 = 0.008
            if pity_5 >= 66:
                rate_5 = 0.008 + (pity_5 - 65) * 0.066
            
            if pity_5 == 80 or random.random() < rate_5:
                pity_5 = 0
                is_pickup = False
                if guaranteed:
                    is_pickup = True
                    guaranteed = False
                else:
                    if random.random() < 0.5:
                        is_pickup = True
                    else:
                        guaranteed = True
                
                if is_pickup:
                    stats["pickup_5"] += 1
                    if int(stats["pickup_5"]) == 1:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 픽업 획득 (현재 명함)")
                    else:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 픽업 획득 (현재 {int(stats['pickup_5'])-1}번)")
                else:
                    stats["other_5"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 상시 획득 (픽뚫)")
                continue
            
            # 4성: 6.0% 확률
            if pity_4 >= 10 or random.random() < 0.06:
                stats["4_star"] += 1
                pity_4 = 0
                
        return stats