import random
from simulator.games._base import Game

# 기본확률 0.8%
# 66회부터 확률 증가
# 80회 천장
# 대충 아래 내용이 맞다고 치고 로직 재구성
# 3줄 요약

# (1) 5성 확률은 1.848%라서 평균적으로 55연차에 5성 1개 먹음
# 즉 픽뚫없는 무기는 55연차가 기댓값이고 픽뚫있는 캐릭은 82.5연차가 기댓값임

# (2) 확업구간 스타트는 66뽑임
# 즉 65뽑까지 안나왔으면 그 이후부터 잘 튀어나오니까 조심해서 돌리셈

# (3) 확업구간은 총 3구간으로 나뉨
# 66~70뽑 4%씩 증가,
# 71~75뽑 8%씩 증가,
# 76~78뽑 10%씩 증가,
# 79뽑에 나올 확률은 100%
# 80뽑에 나올 확률은 없음 불가능함
class WutheringWaves(Game):
    def run_simulation(self, target_rank):
        # 6보다 큰 타겟 돌파가 들어오면 6돌로 강제 고정
        if target_rank > 6:
            target_rank = 6
            
        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                 "total_pulls": 0,
                 "pickup_5": 0,
                 "other_5": 0,
                 "4_star": 0,
                 "weapon_3": 0,
                 "crumbs": 0,
                 "log": []}
        
        stack_5 = 0
        stack_4 = 0
        char_up_4 = 0 # 4성 확률업 캐릭터... 실제 캐릭터 목록을 다 넣을건 아니니까 4성 확업캐를 풀돌한 다음부터는 부스러기 8개 주는 식으로 계산
        guaranteed = False
        
        while stats["pickup_5"] < target_copies:
            stats["total_pulls"] += 1
            stack_5 += 1
            stack_4 += 1
            
            curr_random = random.random()
            
            rate_5 = 0.008
            if 66 <= stack_5 < 71:
                rate_5 = 0.008 + (stack_5 - 65) * 0.04
            elif 71 <= stack_5 < 76:
                rate_5 = 0.208 + (stack_5 - 70) * 0.08
            elif 76 <= stack_5 < 80:
                rate_5 = 0.608 + (stack_5 - 75) * 0.1
            
            if stack_5 == 80 or curr_random < rate_5:
                stack_5 = 0
                stats["crumbs"] += 15
                is_pickup = False
                if guaranteed:
                    is_pickup = True
                    guaranteed = False
                else:
                    if random.choice([True, False]):
                        is_pickup = True
                    else:
                        guaranteed = True
                
                if is_pickup:
                    stats["pickup_5"] += 1
                    if int(stats["pickup_5"]) == 1:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 픽업 획득 (명함)")
                    else:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 픽업 획득 ({int(stats['pickup_5'])}번 획득: {int(stats['pickup_5'])-1}돌)")
                else:
                    stats["other_5"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 상시 획득 (픽뚫)")
                continue
            
            # 4성: 6.0% 확률, 10회차 확정
            if stack_4 >= 10 or curr_random < 0.06:
                stats["4_star"] += 1
                stats["crumbs"] += 3
                stack_4 = 0
                if random.choice([True, False]):
                    char_up_4 += 1
                    if char_up_4 >= 8:
                        stats["crumbs"] += 5 # 4성 확업캐 풀돌 후부터는 조각 8개
                continue
            
            # 나머지는 3성 무기
            stats["weapon_3"] += 1
                
        return stats