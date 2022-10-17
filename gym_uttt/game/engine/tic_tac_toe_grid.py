from typing import List

import numpy as np
from gym.error import InvalidAction

from gym_uttt.game.engine.action import Action


class TicTacToeGrid:
    orig_x: int
    orig_y: int
    cell_size: int
    grid: np.array = np.zeros((3, 3))
    winner: int = 0

    def get_valid_actions(self) -> List[Action]:
        valid_actions = []
        if self.winner == 0:
            for x in range(3):
                for y in range(3):
                    valid_actions.append(Action(x, y, None))
        return valid_actions

    def play(self, action: Action) -> int:
        if (not (3 > action.row > 0)) or (not (3 > action.col > 0)) or self.grid[action.row, action.col] != 0:
            raise InvalidAction("Invalid move!")

        # update grid
        self.grid[action.row][action.col] = action.player
        winner = self.check_winner()
        return winner

    def check_winner(self) -> int:
        grid = self.grid
        for i in range(3):
            # check rows
            if (grid[i, 0] > 0) and (grid[i, 0] == grid[i, 1]) and (grid[i, 0] == grid[i, 2]):
                return grid[i, 0]

            # check cols
            if (grid[0, i] > 0) and (grid[0, i] == grid[1, i]) and (grid[0][i] == grid[2][i]):
                return grid[0, i]

        # check diags
        if (grid[0, 0] > 0) and (grid[0, 0] == grid[1, 1]) and (grid[0, 0] == grid[2, 2]):
            return grid[0, 0]
        if (grid[2, 0] > 0) and (grid[2, 0] == grid[1, 1]) and (grid[2, 0] == grid[0][2]):
            return grid[2, 0]

        return 0
