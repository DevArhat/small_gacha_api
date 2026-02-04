from .._base import Game
import random

# 5성 관련 확률 정리
# 기본확률 0.6%
# 74회부터 확률 증가 - 유저 추정치?
# 90회 천장
# 반천 50:50
# 별빛 포착: 반천 픽뚫을 3번 당하면 다음 반천을 확천으로 바꿔주는 시스템이라고 함....
# 확정적으로 확률공지가 나온 시스템이 아니라서 좀더 찾아봐야될듯

# 4성 관련 확률 정리
# 기본확률 5.1%
# 10회 천장 있음
# 반천-확천 사이클 있음

# 공통사항
# 캐릭터 명함 -> 뽑기 환급재료 지급 없음
# 5성 중복 캐릭터 -> 스타라이트 10개
# 4성 중복 캐릭터 -> 스타라이트 2개
# 5성 풀돌 캐릭터 -> 스타라이트 25개
# 4성 풀돌 캐릭터 -> 스타라이트 5개
# 4성 무기 -> 스타라이트 2개
# 3성 무기 -> 스타더스트 15개
# 5성 픽뚫은 중복으로 가정
# 4성 확률업 캐릭터는 풀돌, 아닌 캐릭터는 단순중복으로 가정
# 스타더스트 뽑기재화는 월간 5개만 교환 가능하므로 굳이 고려하지 않았음

# 교환비
# 스타라이트 5개 -> 뽑기권 1
# 스타더스트 75개 -> 뽑기권 1 (월간 5회 제한)
# 160 원석 -> 뽑기권 1
# 119,000 KRW -> 8080 원석 = 약 50.5 뽑기권

class GenshinImpact(Game):
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
                    if random.choice([True, False]):
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
            # 5.1% 확률, 10회차에 확정,
            # 반천 확천 사이클 있음, 5.1%를 캐릭터랑 무기가 반반 나눠가짐
            # 4성 획득 시 50% 확률로 확률업 4성
            # 근데 이 말대로면 캐릭터가 나오는 파이를 확률업 캐릭터가 다 먹고 있는데,
            # 4성에도 캐릭터 확률이 점점 올라가는 로직이 있나?
            # 그렇게 되면 만약에 캐릭터가 3%, 무기가 2.55% 이렇게 올라갔다고 쳤을 때
            # 4성 획득 확률에서 50%를 떼어내도 캐릭터쪽에 파이가 좀 있으니까, 확률업이 아닌 4성 캐가 나오는게 설명이 되지 않나 싶음..
            rate_4 = 0.051
            if stack_4 >= 10 or random.random() < rate_4:
                stats["4_star"] += 1
                stack_4 = 0
                continue
            # 나머지는 3성 무기
            stats["weapon_3"] += 1
                
        return stats
