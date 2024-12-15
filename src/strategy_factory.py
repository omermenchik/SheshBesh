from src.compare_all_moves_strategy import CompareAllMovesSimple,CompareAllMovesMinMax
from src.strategies import MoveFurthestBackStrategy, HumanStrategy, MoveRandomPiece


class StrategyFactory:
    @staticmethod
    def create_by_name(strategy_name, time_limit=5):
        for strategy in StrategyFactory.get_all():
            if strategy.__name__ == strategy_name:
                # Pass time_limit and depth only to relevant strategies
                if strategy in [CompareAllMovesSimple, CompareAllMovesMinMax]:
                    return strategy(time_limit=time_limit)
                return strategy()

        raise Exception(f"Cannot find strategy {strategy_name}")

    @staticmethod
    def get_all():
        strategies = [
            MoveRandomPiece,
            MoveFurthestBackStrategy,
            CompareAllMovesSimple,
            HumanStrategy,
            CompareAllMovesMinMax,
        ]
        return strategies
