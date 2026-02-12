import random
from simulator.games._base import Game
from simulator.games.kurogames import arrange_stats

# 기본확률 0.8%
# 66회부터 확률 증가
# 80회 천장
# 4성 기본확률 6%, 4성천장(10회)있음, 4성확률업 반천/확천 있음

# 산호 관련
# 5성 1~7회차 획득: 15개
# 5성 8~회차 획득: 40개
# 5성 픽뚫일 경우 각 항목에 +30개 (풀돌픽뚫나면 70개임 ㄷㄷ)
# 4성 1~7회차 획득: 3개
# 4성 8~회차 획득: 8개
# 4성 무기: 3개

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
        crumbs_exchanged = 0
        guaranteed = False
        guaranteed_4 = False
        
        while stats["pull_result"]["pickup_5"] < target_copies:
            
            if stats['crumbs']['total'] >= 360 and crumbs_exchanged < 2 and not("미교환" in self.game_name):
                stats['pull_result']['pickup_5'] += 1
                stats['crumbs']['total'] -= 360
                crumbs_exchanged += 1
                stats['logs']['log'].append(f"[Pull {stats['raw']['pulls']}] 산호{crumbs_exchanged} 교환 완료 ({int(stats['pull_result']['pickup_5'])}번 획득: {int(stats['pull_result']['pickup_5'])-1}돌)")
                stats['logs']['target'].append(f"산호{crumbs_exchanged}")
                if stats['pull_result']['pickup_5'] >= target_copies:
                    break
                
            stats["raw"]["pulls"] += 1
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
                stack_4 = 0
                stats["crumbs"]["total"] += 15
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
                        stats["logs"]["log"].append(f"[Pull {stats["raw"]["pulls"]}] 5★ 픽업 획득 (명함)")
                        stats["logs"]["target"].append(f"{stats["raw"]["pulls"]}")
                    else:
                        stats["logs"]["log"].append(f"[Pull {stats["raw"]["pulls"]}] 5★ 픽업 획득 ({int(stats['pull_result']['pickup_5'])}번 획득: {int(stats['pull_result']['pickup_5'])-1}돌)")
                        stats["logs"]["target"].append(f"{stats["raw"]["pulls"]}")
                else:
                    stats['pull_result']["other_5"] += 1
                    stats["crumbs"]["total"] += 30
                    stats["logs"]["log"].append(f"[Pull {stats["raw"]["pulls"]}] 5★ 상시 획득 (픽뚫)")
                continue
            
            # 4성: 6.0% 확률, 10회차 확정
            # 그냥 호요버스겜쪽에 세팅한것처럼
            # 4성캐 다 풀돌이라 치고 일단 8개 튀어나오고
            # 25% 확률로 무기 떠서 3개만 나오고
            # 대충 그렇게 구성
            if stack_4 >= 10 or curr_random < 0.06:
                stats["pull_result"]["4_star"] += 1
                stats["crumbs"]["total"] += 8
                stack_4 = 0
                if guaranteed_4 or random.choice([True, False]):
                     guaranteed_4 = False
                else:
                    guaranteed_4 = True
                    if random.choice([True, False]):
                        stats["crumbs"]["total"] -= 5
                    
                continue
            
            # 나머지는 3성 무기
            stats['pull_result']["weapon_3"] += 1
        
        return arrange_stats(stats, 8)