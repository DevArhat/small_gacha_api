import random
from .base import Game

class Arknights(Game):
    def run_simulation(self, target_rank):
        # 명일방주: 2.0% / 50회 soft pity / 99회 hard pity
        # 한정 픽업: 6성 중 35% 확률 (이중 픽업 기준, 단독이면 50%지만 보통 한정이므로 35% 가정)
        # 천장(Spark): 300회 뽑기 시 정가 (토큰 소모)
        target_copies = target_rank + 1
        stats = {"game": "Arknights", "total_pulls": 0, "pickup_6": 0, "other_6": 0, 
                 "5_star": 0, "4_star": 0, "spark_count": 0, "log":[]}
        
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
            
            # 하위 등급 (5성: 8%, 4성: 50%) - 10회 확정은 첫 10회만 적용되므로 반복 시뮬레이션에선 단순 확률 적용
            rnd = random.random()
            if rnd < 0.08:
                stats["5_star"] += 1
            elif rnd < 0.08 + 0.50:
                stats["4_star"] += 1
                
        return stats