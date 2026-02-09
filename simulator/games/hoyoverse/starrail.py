from simulator.games._base import Game
import random

# 5성 관련 확률 정리
# 기본확률 0.6%
# 74회부터 확률 증가 - 유저 추정치?
# 90회 천장
# 반천 50:50

# 4성 관련 확률 정리
# 기본확률 5.1%
# 10회 천장 있음
# 반천-확천 사이클 있음

# 공통사항
# 캐릭터 최초획득 -> 뽑기 환급재료 지급 없음
# 5성 중복 캐릭터 -> 스타라이트 40개
# 4성 중복 캐릭터 -> 스타라이트 8개
# 5성 풀돌 캐릭터 -> 스타라이트 100개
# 4성 풀돌 캐릭터 -> 스타라이트 20개
# 4성 광추 -> 스타라이트 8개
# 3성 광추 -> 잔화 20개
# 5성 픽뚫은 중복으로 가정
# 4성 캐릭터는 풀돌 상태로 가정
# 스타더스트 뽑기권은 월간 5개만 교환 가능하므로 굳이 고려하지 않았음

# 교환비
# 스타라이트 20개 -> 뽑기권 1
# 잔화 90개 -> 뽑기권 1 (월간 5회 제한)
# 160 성옥 -> 뽑기권 1
# 119,000 KRW -> 8080 성옥 = 약 50.5 뽑기권

class HonkaiStarRail(Game):
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
                 "log":[]}
        
        stack_5 = 0
        stack_4 = 0
        guaranteed = False
        
        while stats["pickup_5"] < target_copies:
            stats["total_pulls"] += 1
            stack_5 += 1
            stack_4 += 1
            
            # 이번 회차의 랜덤 숫자 발급
            curr_random = random.random()
            
            # 5성 확률 계산
            rate_5 = 0.006
            if stack_5 >= 74:
                rate_5 = 0.006 + (stack_5 - 73) * 0.06
            
            # 5성 획득 판정
            if stack_5 == 90 or curr_random < rate_5:
                stack_5 = 0
                stats["crumbs"] += 40
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
                        stats["crumbs"] += 40
                else:
                    stats["other_5"] += 1
                    stats["log"].append(f"[Pull {stats['total_pulls']}] 5★ 상시 획득 (픽뚫)")
                    stats["crumbs"] += 40
                continue
            
            # 4성 획득 판정 (10회 천장)
            # 5.1% 확률, 10회차에 확정
            # 반천 확천 사이클 있음, 확업4성캐랑 기타4성(캐릭+광추)전체 가 반반 나눠가짐
            # 4성 획득 시 50% 확률로 확률업 4성
            # 위의 내용은 무시하고 모든 4성 캐릭터는 풀돌 상태인 걸로 가정
            # 4성 아이템 비중에서 광추랑 캐릭터가 반반갈라 파이 먹고 있다고 치고
            # 4성 획득 중에서 25% 확률로는 광추가 떠서 스타라이트가 8개만 나왔다고 시뮬레이트
            # 더 좋은 예측 모델이 있으면 스타라이트 관련된 부분은 수정 필요함
            rate_4 = 0.051
            if stack_4 >= 10 or curr_random < rate_4:
                stats["4_star"] += 1
                stats["crumbs"] += 20
                stack_4 = 0
                # 광추가 떴는지 캐릭터가 떴는지 판단하는 랜덤숫자
                if random.random() < 0.25:
                    stats["crumbs"] -= 12
                continue
            # 나머지는 그냥 '광추'로 처리
            stats["weapon_3"] += 1
                
        return stats
  