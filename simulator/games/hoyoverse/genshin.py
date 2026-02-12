from simulator.games._base import Game
import random

from simulator.games.hoyoverse import arrange_stats

# 5성 관련 확률 정리
# 기본확률 0.6%
# 74회부터 확률 증가 - 유저 추정치
# 90회 천장
# 반천 50:50
# 별빛 포착: 반천 픽뚫을 3번 당하면 다음 반천을 확천으로 바꿔주는 시스템이라고 함....
# 확정적으로 확률공지가 나온 시스템이 아니라서 좀더 찾아봐야될듯
# 지금까지 커뮤니티에서 분석된 내용:
# 반천장 5성 캐릭터 뽑기에 진입하는 순간 기준,
# 0스택 0.018%, 1스택 5%, 2스택 10%, 3스택 50% 추가 (1/2스택일 때의 확률 불명, 3스택일 땐 50+50 해서 100%)
# 확천이 아닐 때 픽업 캐릭터를 획득하면 1스택 감소 (0 미만으로 감소하지 않음)
# 픽뚫이 나면 1스택 증가

# 4성 관련 확률 정리
# 기본확률 5.1%
# 10회 천장 있음
# 반천-확천 사이클 있음

# 공통사항
# 캐릭터 최초획득 -> 뽑기 환급재료 지급 없음
# 5성 중복 캐릭터 -> 스타라이트 10개
# 4성 중복 캐릭터 -> 스타라이트 2개
# 5성 풀돌 캐릭터 -> 스타라이트 25개
# 4성 풀돌 캐릭터 -> 스타라이트 5개
# 4성 무기 -> 스타라이트 2개
# 3성 무기 -> 스타더스트 15개
# 5성 픽뚫은 중복으로 가정
# 4성 캐릭터는 풀돌 상태로 가정
# 스타더스트 뽑기권은 월간 5개만 교환 가능하므로 굳이 고려하지 않았음

# 교환비
# 스타라이트 5개 -> 뽑기권 1
# 스타더스트 75개 -> 뽑기권 1 (월간 5회 제한)
# 160 원석 -> 뽑기권 1
# 119,000 KRW -> 8080 원석 = 약 50.5 뽑기권

class GenshinImpact(Game):
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
        
        # 별빛 포착 스택용 변수
        # 이 시뮬레이터에서 별빛포착 확률 모델은
        # https://www.reddit.com/r/Genshin_Impact/comments/1hd1sqa/understanding_genshin_impacts_capturing_radiance/
        # https://preview.redd.it/understanding-genshin-impacts-capturing-radiance-in-depth-v0-a640fhy4yi6e1.png?width=1080&crop=smart&auto=webp&s=9d2d714427299718b0296c55ae3c9dd0d64975e6
        # 위의 reddit 글과 이미지를 기반으로 했음
        # 해당 모델에 따르면, 스택은 0~3 범위에서 동작하지만 기본값은 1임
        capturing_radiance_stack = 1
        
        while stats['pull_result']["pickup_5"] < target_copies:
            stats['raw']['pulls'] += 1
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
                is_pickup = False
                
                if guaranteed:
                    is_pickup = True
                    guaranteed = False
                else:
                    if random.choice([True, False]):
                        is_pickup = True
                        capturing_radiance_stack = minus_stack(capturing_radiance_stack)
                    else:                          
                        radiance_result = handle_radiance(capturing_radiance_stack)
                        is_pickup, capturing_radiance_stack = radiance_result
                        if is_pickup:
                            stats['pull_result']["pickup_5"] += 1
                            if int(stats['pull_result']["pickup_5"]) == 1:
                                stats['logs']["log"].append(f"[Pull {stats['raw']['pulls']}] 별빛 포착! 5★ 픽업 획득 (명함)")
                                stats['logs']['target'].append(f"R{stats['raw']['pulls']}")
                            else:
                                stats['logs']["log"].append(f"[Pull {stats['raw']['pulls']}] 별빛 포착! 5★ 픽업 획득 ({int(stats['pull_result']['pickup_5'])}번 획득: {int(stats['pull_result']['pickup_5'])-1}돌)")
                                stats['logs']['target'].append(f"R{stats['raw']['pulls']}")
                                stats["crumbs"]['total'] += 10
                        else:
                            stats['pull_result']["other_5"] += 1
                            stats['logs']["log"].append(f"[Pull {stats['raw']['pulls']}] 5★ 상시 획득 (픽뚫)")
                            stats["crumbs"]['total'] += 10
                            guaranteed = True
                        continue
                            
                if is_pickup:
                    stats['pull_result']["pickup_5"] += 1
                    if int(stats['pull_result']["pickup_5"]) == 1:
                        stats['logs']["log"].append(f"[Pull {stats['raw']['pulls']}] 5★ 픽업 획득 (명함)")
                        stats['logs']['target'].append(f"{stats['raw']['pulls']}")
                    else:
                        stats['logs']["log"].append(f"[Pull {stats['raw']['pulls']}] 5★ 픽업 획득 ({int(stats['pull_result']['pickup_5'])}번 획득: {int(stats['pull_result']['pickup_5'])-1}돌)")
                        stats['logs']['target'].append(f"{stats['raw']['pulls']}")
                        stats["crumbs"]['total'] += 10
                else:
                    stats['pull_result']["other_5"] += 1
                    stats['logs']["log"].append(f"[Pull {stats['raw']['pulls']}] 5★ 상시 획득 (픽뚫)")
                    stats["crumbs"]['total'] += 10
                continue
            
            # 4성 획득 판정 (10회 천장)
            # 5.1% 확률, 10회차에 확정
            # 반천 확천 사이클 있음, 확업4성캐랑 기타4성 전체가 반반 나눠가짐
            # 4성 획득 시 50% 확률로 확률업 4성
            # 위의 내용은 무시하고 모든 4성 캐릭터는 풀돌 상태인 걸로 가정
            # 4성 아이템 비중에서 무기랑 캐릭터가 반반갈라 파이 먹고 있다고 치고
            # 4성 획득 중에서 25% 확률로는 무기가 떠서 스타라이트가 2개만 나왔다고 시뮬레이트
            # 더 좋은 예측 모델이 있으면 스타라이트 관련된 부분은 수정 필요함
            rate_4 = 0.051
            if stack_4 >= 10 or curr_random < rate_4:
                stats["pull_result"]["4_star"] += 1
                stats["crumbs"]['total'] += 5
                stack_4 = 0
                # 무기가 떴는지 캐릭터가 떴는지 판단하는 랜덤숫자는 메인 뽑기 확률과 별개
                if random.random() < 0.25:
                    stats["crumbs"]['total'] -= 3
                continue
            # 나머지는 3성 무기
            stats["pull_result"]["weapon_3"] += 1
                
        return arrange_stats(stats, 5)


def minus_stack(radiance_stack) -> int:
    """
    별빛포착 스택을 빼기 위한 함수
    본 시뮬레이션에 적용한 모델에 따르면,
    기본값은 1이며 반천 픽업에 성공할 때마다 스택이 내려가지만 0 미만으로 내려가지는 않으므로,
    반복적인 사용을 위해 capturing_radiance_stack -= 1 로 계산하지 않고 별도 함수를 사용함

    Args:
        radiance_stack (_int_): 원본 별빛포착 스택

    Returns:
        new_stack (_int_): 뺄셈 진행 후 별빛포착 스택 (최소치 0)
    """
    # if radiance_stack <= 0:
    #     return radiance_stack
    # else:
    #     return radiance_stack - 1
    return max(0, radiance_stack - 1)

# 종합 픽업 확률이 55% 쯤 나와야되는데
# 시뮬레이션 돌려보니까 56% 미만이 거의 안나옴..
# 좀더 세부적인 로직이 밝혀지면 고쳐봐야될듯
def handle_radiance(radiance_stack: int) -> tuple[bool, int]:
    """
    입력된 radiance stack에 따라 별빛포착 랜덤발동 성공 여부와 새로운 radiance stack을 반환하는 함수
    
    :param radiance_stack: 현재 별빛포착 스택
    :type radiance_stack: int
    :return: 별빛포착 발동 여부 , 계산 후 별빛포착 스택
    :rtype: is_radiance_captured, new_stack: tuple[bool, int]
    """
    if radiance_stack == 0:
        if random.random() < 0.00018:
            return (True, 0)
        else: 
            return (False, 1)
    elif radiance_stack == 1:
        if random.random() < 0.05:
            return (True, 0)
        else:
            return (False, radiance_stack+1)
    elif radiance_stack == 2:
        if random.random() < 0.1:
            return (True, 0)
        else:
            return (False, radiance_stack+1)
    elif radiance_stack == 3:
        return (True, 1)
    else:
        return (False, radiance_stack)
    
        