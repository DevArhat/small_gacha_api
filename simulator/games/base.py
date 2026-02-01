from abc import ABC, abstractmethod

class Game(ABC):
    @abstractmethod
    def run_simulation(self, target_rank: int) -> dict:
        """각 게임별 구체적인 뽑기 로직"""
        pass