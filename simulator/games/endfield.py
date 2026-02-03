import random
from ._base import Game

# 기본확률 0.8%
# 65회부터 확률 증가
# 120회 확정 (1회 only)
# 240회 확정 (돌파권 지급)
# 6성 -> 무뽑재료 2000
# 5성 -> 무뽑재료 200
# 4성 -> 무뽑재료 20
class Endfield(Game):
    def run_simulation(self, target_rank):
        # 명방은 풀돌이 5잠재라서 그 이상이 들어오면 강제로 5돌로 고정함
        if target_rank > 5:
            target_rank = 5
            
        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                 "total_pulls": 0,
                 "pickup_6": 0,
                 "other_6": 0, 
                 "5_star": 0,
                 "4_star": 0, 
                 "log": []}
        
        stacks = 0
        guarantee_120_counter = 0
        guarantee_240_counter = 0
        used_120_guarantee = False 
        
        while stats["pickup_6"] < target_copies:
            stats["total_pulls"] += 1
            stacks += 1
            guarantee_120_counter += 1
            guarantee_240_counter += 1
            rnd = random.random()
            
            # 긴급모집
            # 30회 뽑기 시 10회 무료,
            # 다른 모든 스택과 무관하므로 긴급모집 로직 종료 후 continue하지 않음
            # 단, 긴급모집 후 대상 copy 수가 만족되었을 경우 메인 while문을 탈출
            if stacks == 30:
                # 긴급모집 10회 중 5성 1회 확정
                emergency_5star = False
                
                for i in range(10):
                    if rnd < 0.008:
                        if random.choice([True, False]):
                            stats["pickup_6"] += 1
                            # 픽업 획득 시 120 카운터 초기화
                            guarantee_120_counter = 0
                            used_120_guarantee = True # 1회용
                    
                            if int(stats["pickup_6"]) == 1:
                                stats["log"].append(f"[긴급 {i+1}] 6★ 픽업 획득 (현재 명함)")
                            else:
                                stats["log"].append(f"[긴급 {i+1}] 6★ 픽업 획득 (현재 {int(stats['pickup_6'])}번 획득: {int(stats['pickup_6'])-1}돌)")
                    
                        else:
                            stats["other_6"] += 1
                            stats["log"].append(f"[긴급 {i+1}] 6★ 상시 획득 (픽뚫)")
                        continue
                    
                    if rnd < 0.08:
                        stats["5_star"] += 1
                        emergency_5star = True
                
                if not emergency_5star:
                    stats["5_star"] += 1
    
                if stats["pickup_6"] >= target_copies:
                    break
                

            
            # 240회 보너스 (돌파권) 체크
            if guarantee_240_counter == 240:
                stats["pickup_6"] += 1
                guarantee_240_counter = 0
                stats["log"].append(f"[Pull {stats['total_pulls']}] 240뽑 돌파권 획득 (현재 {int(stats['pickup_6'])}번 획득: {int(stats['pickup_6'])-1}돌)")
                if stats["pickup_6"] >= target_copies:
                    break

            # 120회 확정 체크
            if guarantee_120_counter == 120 and not used_120_guarantee:
                stats["pickup_6"] += 1
                used_120_guarantee = True # 1회용
                guarantee_120_counter = 0
                stacks = 0 # 6성 획득이므로 천장스택 리셋
                stats["log"].append(f"[Pull {stats['total_pulls']}] 120뽑 확정명함 획득")
                continue

            # 6성 확률 계산
            rate_6 = 0.008
            if stacks >= 65:
                rate_6 = 0.008 + (stacks - 65) * 0.05
            
            if stacks == 80 or rnd < rate_6:
                stacks = 0
                # 50/50 확률
                if random.choice([True, False]):
                    stats["pickup_6"] += 1
                    # 픽업 획득 시 120 카운터 초기화
                    guarantee_120_counter = 0
                    used_120_guarantee = True # 1회용
                    if int(stats["pickup_6"]) == 1:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ 픽업 획득 (현재 명함)")
                    else:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ 픽업 획득 (현재 {int(stats['pickup_6'])}번 획득: {int(stats['pickup_6'])-1}돌)")
                else:
                    stats["other_6"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ 상시 획득 (픽뚫)")
                continue

            # 5성 (8%)
            if rnd < 0.08:
                stats["5_star"] += 1
                continue
            # 4성 (기본 91.2%, 암튼 여기까지 왔으면 4성)
            stats["4_star"] += 1
            continue
                
        return stats