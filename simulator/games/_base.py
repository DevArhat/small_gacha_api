from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, game_name: str = "붕괴: 스타레일"):
        self.game_name = game_name
    
    @abstractmethod
    def run_simulation(self, target_rank: int) -> dict:
        """게임별 가챠로직 추상메서드"""
        pass