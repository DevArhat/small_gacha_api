import random
from ._base import Game

class Endfield(Game):
    def run_simulation(self, target_rank):
        # 엔드필드: 0.8% / 65회 soft / 80회 hard / 50:50
        # 120회 확정 (1회 only)
        # 240회 확정 (재료 아이템 = 1돌파 취급)
        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                 "total_pulls": 0,
                 "pickup_6": 0,
                 "other_6": 0, 
                 "5_star": 0,
                 "4_star": 0, 
                 "log": []}
        
        pity_6 = 0
        guarantee_120_counter = 0
        guarantee_240_counter = 0
        used_120_guarantee = False 
        
        while stats["pickup_6"] < target_copies:
            stats["total_pulls"] += 1
            pity_6 += 1
            guarantee_120_counter += 1
            guarantee_240_counter += 1
            rnd = random.random()
            
            # 240회 보너스 (돌파권) 체크
            if guarantee_240_counter == 240:
                stats["pickup_6"] += 1
                guarantee_240_counter = 0
                stats["log"].append(f"[Pull {stats['total_pulls']}] 240뽑 돌파권 획득")
                if stats["pickup_6"] >= target_copies:
                    break

            # 120회 확정 체크
            if guarantee_120_counter == 120 and not used_120_guarantee:
                stats["pickup_6"] += 1
                used_120_guarantee = True # 1회용
                guarantee_120_counter = 0
                pity_6 = 0 # 6성 획득이므로 천장스택 리셋
                stats["log"].append(f"[Pull {stats['total_pulls']}] 120뽑 확정명함 획득")
                continue

            # 6성 확률 계산
            rate_6 = 0.008
            if pity_6 >= 65:
                rate_6 = 0.008 + (pity_6 - 64) * 0.05
            
            if pity_6 == 80 or rnd < rate_6:
                pity_6 = 0
                # 50/50 확률
                if random.choice([True, False]):
                    stats["pickup_6"] += 1
                    # 픽업 획득 시 120 카운터 초기화
                    guarantee_120_counter = 0
                    used_120_guarantee = True # 1회용
                    if int(stats["pickup_6"]) == 1:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ 픽업 획득 (현재 명함)")
                    else:
                        stats["log"].append(f"[Pull {stats['total_pulls']}] 6★ 픽업 획득 (현재 {int(stats['pickup_6'])-1}돌)")
                else:
                    stats["other_6"] += 1
                    # 픽뚫 시에는 120 카운터 유지됨
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