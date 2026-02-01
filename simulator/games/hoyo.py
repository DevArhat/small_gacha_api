import random
from .base import Game

class HoyoverseGames(Game):
    def run_simulation(self, target_rank):
        # 원신: 0.6% / 74회 soft pity / 90회 hard pity / 4성 10회 천장
        target_copies = target_rank + 1
        stats = {"game": "Genshin", "total_pulls": 0, "pickup_5": 0, "other_5": 0, "4_star": 0, "log":[]}
        
        pity_5 = 0
        pity_4 = 0
        guaranteed = False
        
        while stats["pickup_5"] < target_copies:
            stats["total_pulls"] += 1
            pity_5 += 1
            pity_4 += 1
            
            # 5성 확률 계산
            rate_5 = 0.006
            if pity_5 >= 74:
                rate_5 = 0.006 + (pity_5 - 73) * 0.06
            
            # 5성 획득 판정
            if pity_5 == 90 or random.random() < rate_5:
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
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ PICKUP Obtained (Copies: {stats['pickup_5']})")
                else:
                    stats["other_5"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ Standard Character (Spook)")
                continue # 5성이 나오면 4성 체크 건너뜀
            
            # 4성 획득 판정 (10회 천장)
            # 5.1% 확률. 10회차에 확정.
            rate_4 = 0.051
            if pity_4 >= 10 or random.random() < rate_4:
                stats["4_star"] += 1
                pity_4 = 0
                
        return stats
    