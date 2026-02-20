from .games import get_game_strategy

class GachaSimulator:
    def simulate(self, game_name: str, target_rank: int):
        game_strategy = get_game_strategy(game_name)
        return game_strategy.run_simulation(target_rank)
    
    def v2_simulate(self, game_name: str, target_rank: int):
        game_strategy = get_game_strategy(game_name)
        return game_strategy.v2_run_simulation(target_rank)