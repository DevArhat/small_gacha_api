import random
from ._base import Game

class Arknights(Game):
    def run_simulation(self, target_rank):

        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                 "total_pulls": 0,
                 "pickup_6": 0,
                 "other_6": 0, 
                 "5_star": 0,
                 "4_star": 0,
                 "spark_count": 0,
                 "log":[]}
        
        pity_6 = 0
        spark_currency = 0
        
        while stats["pickup_6"] < target_copies:
            stats["total_pulls"] += 1
            pity_6 += 1
            spark_currency += 1
            
            # 정가 교환 체크 (300회)
            if spark_currency >= 300:
                stats["pickup_6"] += 1
                stats["spark_count"] += 1
                spark_currency -= 300
                stats["log"].append(f"[Pull {stats['total_pulls']}] Spark Redeemed! (Total Copies: {stats['pickup_6']})")
                if stats["pickup_6"] >= target_copies:
                    break
            
            rate_6 = 0.02
            if pity_6 > 50:
                rate_6 = 0.02 + (pity_6 - 50) * 0.02
            
            # 6성 획득
            if random.random() < rate_6:
                pity_6 = 0
                # 한정 픽업 확률 35% (나머지 65%는 통상 또는 다른 픽업)
                if random.random() < 0.35:
                    stats["pickup_6"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ LIMITED PICKUP Obtained (Copies: {stats['pickup_6']})")
                else:
                    stats["other_6"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ Off-Banner/Other Rate-up")
                continue
            
            # 하위 등급 (5성: 8%, 4성: 50%) - 10회 확정은 나중에 생각해보자
            rnd = random.random()
            if rnd < 0.08:
                stats["5_star"] += 1
            elif rnd < 0.08 + 0.50:
                stats["4_star"] += 1
                
        return stats