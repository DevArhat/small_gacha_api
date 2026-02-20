# 외환 유출 시뮬레이터

## gacha-simulator-api.vercel.app

### 사용법

GET >>> /simulate/{game}/{target_rank}<br>
GET >>> /simulate?game={game}&target_rank={target_rank}<br>
POST >>> /simulate/<br>
POST의 request body는
```json
{
  "game": "string",
  "target_rank": 0
}
```
이렇게생겼음<br>(전 POST 보낼줄 모름.. 그냥 이런것도 있구나 하고 넣어본건데 아시는분은 써먹어보세요)

셋다 기능은 똑같습니다

기본값은 붕스 0돌 (명함)

FastAPI 기반이라서 /docs 하면 swagger 문서를 볼 수 있음
- - -
### {game} : str

| 게임 | 키워드 |
| :--- | :--- |
| 원신 | **gen**, genshin, genshinimpact |
| 붕스 | **hsr**, honkaisr, starrail, honkaistarrail |
| 젠레스 | **zzz**, zen, zenless, zenzero, zenlesszonezero, zenzonezero |
| 명조 | **wuwa**, wutheringwaves |
| 엔필 | **end**, endfield |
| 명조(깡) | wuwa_raw, wutheringwaves_raw |
- - -


### {target_rank} : int

돌파 기준으로 숫자 입력<br>
(이상한거 쓰면 에러뱉음, 음수는 0으로 보정되고 큰 수는 각 게임별 풀돌로 보정됨)

* 명함: 0
* 1돌: 1
* ...
- - -
### 부가기능

GET >>> statistics?game={game}&target_rank={target_rank}

각 게임별/돌파별로 50만번씩 시뮬레이션한 결과 기반 통계<br>
top1, 상위10%, 상위30%, 중간값, 평균, 상위70%, 상위90%, bottom1에 대한 뽑기횟수 / 비용 / 트럭갯수

모든 게임에서 환급 뽑기권이나 명조 산호돌파권 교환 등을 사용하지 않은 기준 (엔드필드 240뽑 돌파권은 일종의 천장이므로 반영되어 있음)
* 파라미터를 모두 비우면 모든 게임 모든 돌파에 대해 나옴 (전체 데이터)
* game 파라미터만 있으면 해당 게임의 0~6(5) 돌파에 대해 나옴
* target_rank 파라미터만 있으면 모든 게임의 해당 돌파에 대해 나옴 (6이면 엔필은 빠짐)
* 게임별 키워드 = gen, hsr, zzz, wuwa, end

실제로 시뮬레이션 돌리면 기다리기 지루하니까<br>
돌려본 결과를 json에 하드코딩해놨음


<br><br>
/list 또는<br>
/list/aliases 에서 구현된 확률모델 목록 확인가능

list의 id로 지정된 항목 뿐 아니라<br>
aliases에 들어있는 영문 모두 사용할 수 있음

맞는 항목이 없으면 기본값은 붕괴스타레일....
- - -
### 응답 형태 예시

JSON 형식으로 반환

#### 원신
(붕괴스타레일, 젠레스존제로도 비슷함 명조도 대충 유사함)

```json
{
  "game": "원신",
  "target_rank": 6,
  "total_pulls": 600,
  "raw": {
    "pulls": 600,
    "cost": 1413862
  },
  "after_exchange": {
    "pulls": 523,
    "cost": 1232416
  },
  "trucks": {
    "raw": 12,
    "after_exchange": 11,
    "raw_cost": 1428000,
    "after_exchange_cost": 1309000
  },
  "pull_result": {
    "pickup_6": 0,
    "other_6": 0,
    "pickup_5": 7,
    "other_5": 3,
    "star_5": 0,
    "star_4": 75,
    "weapon_3": 515
  },
  "crumbs": {
    "total": 387,
    "tickets_changed": 77,
    "remaining": 2
  },
  "logs": {
    "log": [
      "[Pull 3] 5★ 상시 획득 (픽뚫)",
      "[Pull 83] 5★ 픽업 획득 (명함)",
      "[Pull 157] 5★ 상시 획득 (픽뚫)",
      "[Pull 231] 5★ 픽업 획득 (2번 획득: 1돌)",
      "[Pull 306] 별빛 포착! 5★ 픽업 획득 (3번 획득: 2돌)",
      "[Pull 381] 5★ 픽업 획득 (4번 획득: 3돌)",
      "[Pull 436] 5★ 상시 획득 (픽뚫)",
      "[Pull 507] 5★ 픽업 획득 (5번 획득: 4돌)",
      "[Pull 520] 5★ 픽업 획득 (6번 획득: 5돌)",
      "[Pull 600] 5★ 픽업 획득 (7번 획득: 6돌)"
    ],
    "target": ["83", "231", "R306", "381", "507", "520", "600"]
  }
}
```
raw -> pulls = 총 뽑기 횟수 (total_pulls랑 같은 값)<br>
raw -> cost = 뽑기 비용 (뽑기 횟수 기준 추산)

after_exchange -> pulls = 총 뽑기 횟수에서 스타라이트, 잔류신호 등으로 교환 가능한 뽑기권 갯수를 뺀 값<br>
after_exchange -> cost = 그 횟수를 기준으로 추산한 뽑기 비용

trucks -> raw, raw_cost = 총 뽑기 횟수 기준 필요 트럭 갯수, 트럭 기준 비용<br>
trucks -> after_exchange, after_exchange_cost = 페이백 공제 기준 필요 트럭 갯수, 트럭 기준 비용

crumbs -> total = 페이백 뽑기권 교환재료 총 획득 갯수<br>
crumbs -> tickets_changed = 그걸로 바꾼 뽑기권 수<br>
crumbs -> remaining = 남은 페이백 뽑기권 교환재료 수

pull_result -> pickup_6, other_6, star_5 = 여기서는 사용하지 않는 값 (엔드필드 전용)

logs -> log = 5성 획득 로그<br>
logs -> target = 픽업이 뜬 회차<br>
(원신에서 별빛포착으로 먹은 경우 숫자 앞에 R 붙음, 붕/젠은 그런건 딱히 없음)<br>
(명조는 360산호 교환 타이밍에 산호1, 산호2 이렇게 찍힘) -> wuwa_raw로 돌리면 돌파권 교환 빼고 계산 가능


#### 엔드필드

```json
{
  "game": "엔드필드",
  "target_rank": 5,
  "total_pulls": 438,
  "raw": {
    "pulls": 438,
    "cost": 1116900
  },
  "after_exchange": {
    "pulls": 438,
    "cost": 1116900
  },
  "trucks": {
    "raw": 8,
    "after_exchange": 8,
    "raw_cost": 1224000,
    "after_exchange_cost": 1224000
  },
  "pull_result": {
    "pickup_6": 6,
    "other_6": 3,
    "pickup_5": 0,
    "other_5": 0,
    "star_5": 58,
    "star_4": 382,
    "weapon_3": 0
  },
  "crumbs": {
    "total": 37240,
    "tickets_changed": 188,
    "remaining": 16
  },
  "logs": {
    "log": [
      "[긴급 8] 6★ 픽업 획득 (명함)",
      "[Pull 67] 6★ 상시 획득 (픽뚫)",
      "[Pull 120] 6★ 픽업 획득 (확정명함 스택 소진)",
      "[Pull 188] 6★ 픽업 획득 (3번 획득: 2돌)",
      "[Pull 240] 240뽑 돌파권 획득 (4번 획득: 3돌)",
      "[Pull 243] 6★ 상시 획득 (픽뚫)",
      "[Pull 313] 6★ 상시 획득 (픽뚫)",
      "[Pull 366] 6★ 픽업 획득 (5번 획득: 4돌)",
      "[Pull 438] 6★ 픽업 획득 (6번 획득: 5돌)"
    ],
    "target": ["E8", "120", "188", "P240", "366", "438"]
  }
}
```
raw -> pulls = 총 뽑기 횟수 (total_pulls랑 같은 값)<br>
raw -> cost = 뽑기 비용 (뽑기 횟수 기준 추산)

<b>after_exchange -> raw와 동일한 값 반환</b> (뽑기 부산물이 그냥 무기뽑기권이고 캐릭뽑기권 환급식이 아니다보니...)

trucks -> raw, raw_cost = 총 뽑기 횟수 기준 필요 트럭 갯수, 트럭 기준 비용<br>
trucks -> after_exchange, after_exchange_cost : raw와 동일 (after_exchange의 pulls 및 cost와 동일한 이유)<br>
※ 인게임 말고 홈페이지에서 사면 153000원짜리 400오리지늄 상품 있음 그거기준임

<b>crumbs 관련 필드 이름은 그대로지만 의미가 다르므로 주의</b><br>
crumbs -> total = 무기뽑기재료 총 획득 갯수<br>
crumbs -> tickets_changed = 그걸로 무기뽑을 돌릴 수 있는 수<br>
crumbs -> remaining = 남은 무기뽑기재료 수

pull_result -> pickup_5, other_5, weapon_3 = 엔드필드에서는 사용하지 않는 값

logs -> log = 6성 획득 로그<br>
logs -> target = 픽업이 뜬 회차<br>
(긴급모집으로 먹은 경우 E1~E10으로 긴급모집 몇회차에 먹었는지 표시)<br>
(240*n회차 확정돌파권은 P240, P480 이렇게 표시)
- - -
### V2
 
#### /v2/simulate<br>
logs 필드에서 log 필드 삭제<br>
(target, other, total 3개 필드로 구성) -> 픽업 회차만, 픽뚫 회차만, 전체 (설명 없이 뽑기 회차만 str로 제공)

#### /v2/statistics<br>
원/붕/젠 뽑기 부산물 반영<br>
명조 뽑기 부산물 및 산호교환 반영
- - -
### 기본값 관련 주저리...

원신이 기본값이었는데

별빛포착이 좀 복잡한데다 정확한 작동 방식이 알려지지 않았고, 지금 시뮬레이터 확률이 호요버스 공지보다 1%정도 높게 나와서 바꿈
(반천 픽업확률 약 56.2% 나옴, 호요버스 공지는 55%)

원신이랑 확률설정이 비슷하면서 뽑기로직이 직관적이라서 붕스로 함
- - -
명조는 기댓값상 8산호 뽑기권 교환 거르고 360산호 돌파권 사용이 이득 (반박시: 운빨충)<br>
-> 2회까지 360산호가 모이면 무조건 돌파권 교환을 하고, 남은 산호로 8산호 뽑기권 교환을 계산함

단, 'wuwa_raw'를 인수로 넣어줬을 경우 산호 돌파권 교환을 하지 않음
- - -
<br><br>

# DISCLAIMER

- 본 프로젝트는 python 및 fastAPI에 대한 학습 목적으로 구현한 **비공식(Unofficial)** API입니다.
- 본 프로젝트에서 언급되는 게임 명칭, 로직, 데이터 구조 및 관련 에셋에 대한 모든 권리는 각 원저작권자(HoYoverse, KURO GAMES, Hypergryph, GRYPHLINE 등)에게 있습니다.
- 본 프로젝트의 상업적 목적 활용을 권장하지 않으며, 사용 시 반드시 각 원저작권자의 2차 창작 및 저작권 가이드라인을 준수하시기 바랍니다.
