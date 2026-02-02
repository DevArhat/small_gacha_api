import random
from ._base import Game

# 아니 뽑기 구조가 왤케 어려움?
# 6성 반천을 치면 30% 픽뚫 / 35% 픽업대상 / 35% 한정
# 300회 치면 한정 하나 주고 쌓인 뽑기재화로 정가 교환 됨
# '픽업대상' 은 다음 한정픽업부터는 '30% 픽뚫' 에 들어감
# 이 시뮬레이션에선 한정만 노리는 걸로 가정하고, 획득확률을 35%로 설정
class Arknights(Game):
    def run_simulation(self, target_rank):

        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                 "total_pulls": 0,
                 "pickup_6": 0,
                 "other_6": 0, 
                 "5_star": 0,
                 "4_star": 0,
                 "exchange_token": 0,
                 "log":[]}
        
        stacks = 0
        stacks_to_token = 0
        
        while stats["pickup_6"] < target_copies:
            stats["total_pulls"] += 1
            stacks += 1
            spark_currency += 1
            
            # 정가 교환 체크 (300회)
            if stacks_to_token >= 300:
                stats["pickup_6"] += 1
                stats["exchange_token"] += 1
                stacks_to_token -= 300
                stats["log"].append(f"[Pull {stats['total_pulls']}] 풀천장! (현재 {int(stats['pickup_6']) + int(stats['exchange_token'])}회 획득: {int(stats['pickup_6']) + int(stats['exchange_token']) - 1}돌)")
                if stats["pickup_6"] >= target_copies:
                    break
            
            rate_6 = 0.02
            if stacks > 50:
                rate_6 = 0.02 + (stacks - 50) * 0.02
            
            # 6성 획득
            if random.random() < rate_6:
                stacks = 0
                # 한정 픽업 확률 35% (나머지 65%는 통상 또는 다른 픽업)
                if random.random() < 0.35:
                    stats["pickup_6"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ 한정 픽업 획득 (현재 {int(stats['pickup_6']) + int(stats['exchange_token'])}회 획득: {int(stats['pickup_6']) + int(stats['exchange_token']) - 1}돌)")
                else:
                    stats["other_6"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ 상시/기타 픽업 획득")
                continue
            
            # 하위 등급 (5성: 8%, 4성: 50%) - 10회 확정은 나중에 생각해보자
            rnd = random.random()
            if rnd < 0.08:
                stats["5_star"] += 1
            elif rnd < 0.08 + 0.50:
                stats["4_star"] += 1
                
        return stats