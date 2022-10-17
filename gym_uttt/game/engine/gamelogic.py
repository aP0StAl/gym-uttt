from typing import List

from gym_uttt.game.engine.tic_tac_toe_grid import TicTacToeGrid
from gym_uttt.game.engine.action import Action


class TicTacToeGame:
    master_grid: TicTacToeGrid
    small_grids: List[List[TicTacToeGrid]]
    last_action: Action

    def __init__(self):
        pass

    def get_valid_actions(self) -> List[Action]:
        valid_actions = []
        if self.last_action is not None:
            last_action = self.last_action
            grid = self.small_grids[last_action.row % 3][last_action.col % 3]
            for action in grid.get_valid_actions():
                a_row = (last_action.row % 3) * 3 + action.row
                a_col = (last_action.col % 3) * 3 + action.col
                valid_actions.append(Action(a_row, a_col, None))
        if not valid_actions:
            for row in range(3):
                for col in range(3):
                    grid = self.small_grids[row][col]
                    for action in grid.get_valid_actions():
                        a_row = (row % 3) * 3 + action.row
                        a_col = (col % 3) * 3 + action.col
                        valid_actions.append(Action(a_row, a_col, None))
        return valid_actions
