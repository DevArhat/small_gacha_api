import random
from ._base import Game

# 기본확률 0.6%
# 74회부터 확률 증가
# 90회 천장
class HoyoverseGames(Game):
    def run_simulation(self, target_rank):
        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                 "total_pulls": 0,
                 "pickup_5": 0,
                 "other_5": 0,
                 "4_star": 0,
                 "weapon": 0,
                 "log":[]}
        
        stack_5 = 0
        stack_4 = 0
        guaranteed = False
        
        while stats["pickup_5"] < target_copies:
            stats["total_pulls"] += 1
            stack_5 += 1
            stack_4 += 1
            
            # 5성 확률 계산
            rate_5 = 0.006
            if stack_5 >= 74:
                rate_5 = 0.006 + (stack_5 - 73) * 0.06
            
            # 5성 획득 판정
            if stack_5 == 90 or random.random() < rate_5:
                stack_5 = 0
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
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 픽업 획득 (현재 {int(stats['pickup_5'])}번 획득: {int(stats['pickup_5'])-1}돌)")
                else:
                    stats["other_5"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 상시 획득 (픽뚫)")
                continue
            
            # 4성 획득 판정 (10회 천장)
            # 5.1% 확률. 10회차에 확정.
            rate_4 = 0.051
            if stack_4 >= 10 or random.random() < rate_4:
                stats["4_star"] += 1
                stack_4 = 0
                continue
            # 나머지는 그냥 '무기'로 처리 (나중에 개선)
            stats["weapon"] += 1
                
        return stats
    