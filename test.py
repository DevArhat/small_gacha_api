# import simulator_onefile as simulator

# api = simulator.GachaSession()

# while True:
#     result = api.simulate("Endfield", target_rank=2) # 엔드필드 2돌파(3장) 시뮬레이션
#     if 'Pull 120' in str(result['log']):
#         print(result)
#         break

from simulator import GachaSimulator
api = GachaSimulator()

while True:
    result = api.simulate("Endfield", target_rank=2) # 엔드필드 2돌파(3장) 시뮬레이션
    if 'Pull 120' in str(result['log']):
        print(result)
        break