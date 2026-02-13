import random
from simulator.games._base import Game
from simulator.games.hypergryph import end_arrange_stats, init_stats

# 기본확률 0.8%
# 65회부터 확률 증가
# 120회 확정 (1회 only)
# 240회 확정 (돌파권 지급)
# 6성 -> 무뽑재료 2000
# 5성 -> 무뽑재료 200
# 4성 -> 무뽑재료 20
class Endfield(Game):
    def run_simulation(self, target_rank):
        # 0보다 작거나 5보다 큰 타겟 돌파가 들어오면 0 or 5돌로 강제 고정
        target_rank = max(0, min(target_rank, 5))
            
        target_copies = target_rank + 1
        stats = init_stats()
        
        stats['game'] = self.game_name
        stats['target_rank'] = target_rank
        
        stacks = 0
        stacks_5 = 0
        guarantee_120_counter = 0
        guarantee_240_counter = 0
        used_120_guarantee = False 
        
        while stats["pull_result"]["pickup_6"] < target_copies:
            
            # 긴급모집
            # 30회 뽑기 시 10회 무료,
            # 다른 모든 스택과 무관하므로 긴급모집 로직 종료 후 continue하지 않음
            # 단, 긴급모집 후 대상 copy 수가 만족되었을 경우 메인 while문을 탈출
            if stats["raw"]["pulls"] == 30:
                # 긴급모집 10회 중 5성 1회 확정
                emergency_5star = False
                
                for i in range(10):
                    # random을 새로 만들어주지 않았더니 메인 루프에서 만든 랜덤 숫자 그대로 열번 돌아가서 같은 결과로만 복사됨...
                    emergency_rnd = random.random()
                    
                    if emergency_rnd < 0.008:
                        emergency_5star = True
                        if random.choice([True, False]):
                            stats["pull_result"]["pickup_6"] += 1
                            # 외부 스택과 완전 무관함
                            # 픽업 획득 시에도 120회 카운터를 비롯한 스택이 초기화되지 않음
                            stats["logs"]["target"].append(f"E{i+1}")
                            if int(stats["pull_result"]["pickup_6"]) == 1:
                                stats["logs"]["log"].append(f"[긴급 {i+1}] 6★ 픽업 획득 (명함)")
                            else:
                                stats["logs"]["log"].append(f"[긴급 {i+1}] 6★ 픽업 획득 ({int(stats['pull_result']['pickup_6'])}번 획득: {int(stats['pull_result']['pickup_6'])-1}돌)")
                                
                        else:
                            stats["pull_result"]["other_6"] += 1
                            stats["logs"]["log"].append(f"[긴급 {i+1}] 6★ 상시 획득 (픽뚫)")
                    
                    
                    elif emergency_rnd < 0.08:
                        stats["pull_result"]["star_5"] += 1
                        emergency_5star = True
                    
                    else:
                        if i == 9 and not emergency_5star:
                            stats["pull_result"]["star_5"] += 1
                        else:
                            stats["pull_result"]["star_4"] += 1
                
    
                if stats["pull_result"]["pickup_6"] >= target_copies:
                    break
            
                        
            stats["raw"]["pulls"] += 1
            stacks += 1
            stacks_5 += 1
            guarantee_120_counter += 1
            guarantee_240_counter += 1
            rnd = random.random()
                             
            # 240회 보너스 (돌파권) 체크
            if guarantee_240_counter == 240:
                stats["pull_result"]["pickup_6"] += 1
                guarantee_240_counter = 0
                stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] 240뽑 돌파권 획득 ({int(stats['pull_result']['pickup_6'])}번 획득: {int(stats['pull_result']['pickup_6'])-1}돌)")
                stats["logs"]["target"].append(f"P{stats['raw']['pulls']}")
                if stats["pull_result"]["pickup_6"] >= target_copies:
                    break

            # 120회 확정 체크
            if guarantee_120_counter == 120 and not used_120_guarantee:
                stats["pull_result"]["pickup_6"] += 1
                used_120_guarantee = True # 1회용
                guarantee_120_counter = 0
                stacks = 0 # 6성 획득이므로 천장스택 리셋
                stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] 6★ 픽업 획득 (확정명함 스택 소진)")
                stats["logs"]["target"].append(f"{stats['raw']['pulls']}")
                continue

            # 6성 확률 계산
            rate_6 = 0.008
            if stacks >= 65:
                rate_6 = 0.008 + (stacks - 65) * 0.05
            
            if stacks == 80 or rnd < rate_6:
                stacks = 0
                stacks_5 = 0
                if random.choice([True, False]):
                    stats["pull_result"]["pickup_6"] += 1
                    # 픽업 획득 시 120 카운터 초기화
                    guarantee_120_counter = 0
                    if int(stats["pull_result"]["pickup_6"]) == 1 and not used_120_guarantee:
                        stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] 6★ 픽업 획득 (확정명함 스택 소진)")
                        stats["logs"]["target"].append(f"{stats['raw']['pulls']}")
                    else:
                        stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] 6★ 픽업 획득 ({int(stats['pull_result']['pickup_6'])}번 획득: {int(stats['pull_result']['pickup_6'])-1}돌)")
                        stats["logs"]["target"].append(f"{stats['raw']['pulls']}")
                    used_120_guarantee = True # 1회용
                else:
                    stats["pull_result"]["other_6"] += 1
                    stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] 6★ 상시 획득 (픽뚫)")
                continue

            # 5성 (8%)
            if rnd < 0.08 or stacks_5 >= 10:
                stats["pull_result"]["star_5"] += 1
                stacks_5 = 0
                continue
            # 4성 (기본 91.2%, 암튼 여기까지 왔으면 4성)
            stats["pull_result"]["star_4"] += 1
            continue
        
        stats["crumbs"]["total"] = (stats["pull_result"]["pickup_6"] + stats["pull_result"]["other_6"]) * 2000 + stats["pull_result"]["star_5"] * 200 + stats["pull_result"]["star_4"] * 20
                
        return end_arrange_stats(stats)