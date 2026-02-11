import random
from simulator.games._base import Game
from simulator.games.hoyoverse import arrange_stats


# S급 관련 확률 정리
# 기본확률 0.6%
# 74회부터 확률 증가 - 유저 추정치
# 90회 천장
# 반천 50:50

# A급 관련 확률 정리
# 기본확률 9.4%, 캐릭터 7.05%, 엔진 2.35%
# 10회 천장 있음
# 반천-확천 사이클 있음. 반천시 50%로 확업A급
# A급 확률은 젠레스가 표기만 좀 더 자세히 한 거고 종합 확률이 더 높은거지
# A급 안에서의 분배 로직 자체는 원신 붕스랑 같음

# 공통사항
# S급 = 5성, A급 = 4성
# 캐릭터 최초획득 -> 뽑기 환급재료 지급 없음
# S급 중복 캐릭터 -> 잔류신호 40개
# A급 중복 캐릭터 -> 잔류신호 8개
# S급 풀돌 캐릭터 -> 잔류신호 100개
# A급 풀돌 캐릭터 -> 잔류신호 20개
# A급 광추 -> 잔류신호 8개
# 3성 광추 -> 잔향신호 20개
# S급 픽뚫은 중복으로 가정
# A급 캐릭터는 풀돌 상태로 가정
# 잔향 뽑기권은 월간 5개만 교환 가능하므로 굳이 고려하지 않았음

# 교환비
# 잔류신호 20개 -> 뽑기권 1
# 잔향신호 90개 -> 뽑기권 1 (월간 5회 제한)
# 160 폴리그램 -> 뽑기권 1
# 119,000 KRW -> 8080 폴리그램 = 약 50.5 뽑기권

class ZenlessZoneZero(Game):
    def run_simulation(self, target_rank):
        # 0보다 작거나 6보다 큰 타겟 돌파가 들어오면 0 or 6돌로 강제 고정
        target_rank = max(0, min(target_rank, 6))
            
        target_copies = target_rank + 1
        stats = {"game": self.game_name,
                "target_rank": target_rank,                 
                "total_pulls": 0,
                "raw":{
                    "pulls":0,
                    "cost":0,
                    },
                "after_exchange":{
                    "pulls":0,
                    "cost":0,
                    },
                "trucks":{
                    "raw": 0,
                    "after_exchange": 0,
                    "raw_cost": 0,
                    "after_exchange_cost": 0,
                    },
                "pull_result":{
                    "pickup_5": 0,
                    "other_5": 0,
                    "4_star": 0,
                    "weapon_3": 0,
                    },
                "crumbs": {
                    "total": 0,
                    "tickets_changed": 0,
                    "remaining": 0,
                    },
                "logs": {
                    "log": [],
                    "target": [] 
                    }
                }       
        stack_5 = 0
        stack_4 = 0
        guaranteed = False
        
        while stats["pull_result"]["pickup_5"] < target_copies:
            stats["raw"]["pulls"] += 1
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
                stats["crumbs"]['total'] += 40
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
                    stats["pull_result"]["pickup_5"] += 1
                    if int(stats["pull_result"]["pickup_5"]) == 1:
                        stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] S급 픽업 획득 (명함)")
                        stats["logs"]["target"].append(f"{stats['raw']['pulls']}")
                    else:
                        stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] S급 픽업 획득 ({int(stats['pull_result']['pickup_5'])}번 획득: {int(stats['pull_result']['pickup_5'])-1}돌)")
                        stats["crumbs"]['total'] += 40
                else:
                    stats["pull_result"]["other_5"] += 1
                    stats["logs"]["log"].append(f"[Pull {stats['raw']['pulls']}] S급 상시 획득 (픽뚫)")
                    stats["crumbs"]['total'] += 40
                continue
            
            # 4성 획득 판정 (10회 천장)
            # 9.4% 확률, 10회차에 확정
            # 반천 확천 사이클 있음, 확업4성캐랑 기타4성(캐릭+엔진)전체 가 반반 나눠가짐
            # 4성 획득 시 50% 확률로 확률업 4성
            # 모든 4성 캐릭터는 풀돌 상태인 걸로 가정
            # 기타4성 비중에서 엔진이랑 캐릭터가 반반갈라 파이 먹고 있다고 치고
            # 4성 획득 중에서 25% 확률로는 엔진이 떠서 잔류신호가 8개만 나왔다고 시뮬레이트
            # 더 좋은 예측 모델이 있으면 잔류신호 관련된 부분은 수정 필요함
            rate_4 = 0.094
            if stack_4 >= 10 or curr_random < rate_4:
                stats["pull_result"]["4_star"] += 1
                stats["crumbs"]["total"] += 20
                stack_4 = 0
                # 엔진이 떴는지 캐릭터가 떴는지 판단하는 랜덤숫자
                if random.random() < 0.25:
                    stats["crumbs"]["total"] -= 12
                continue
            # 나머지는 그냥 '엔진'으로 처리
            stats["pull_result"]["weapon_3"] += 1
                
        return arrange_stats(stats, 20)
  
 