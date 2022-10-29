import os
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image
from gym.error import InvalidAction

from gym_uttt.game.engine.action import Action

p = Path(__file__).parents[2]
cross = Image.open(os.path.join(p, 'assets/cross.png'))
cross = Image.composite(Image.new('RGBA', cross.size, color='#f1b213'), cross, cross)
circle = Image.open(os.path.join(p, 'assets/circle.png'))
circle = Image.composite(Image.new('RGBA', circle.size, color='#22a1e4'), circle, circle)
small_board = Image.open(os.path.join(p, 'assets/small_board.png'))
small_board.thumbnail((100, 100))
cross_small = cross.copy()
cross_small.thumbnail((24, 24))
circle_small = circle.copy()
circle_small.thumbnail((24, 24))
cross_big = cross.copy()
cross_big.thumbnail((100, 100))
circle_big = circle.copy()
circle_big.thumbnail((100, 100))


class TicTacToeGrid:
    grid: np.array
    winner: int

    def __init__(self):
        self.grid = np.zeros((3, 3), dtype='int8')
        self.winner = 0

    def get_valid_actions(self) -> List[Action]:
        valid_actions = []
        if self.winner == 0:
            for x in range(3):
                for y in range(3):
                    if self.grid[x, y] == 0:
                        valid_actions.append(Action(x, y, None))
        return valid_actions

    def play(self, action: Action) -> int:
        if (not (3 > action.row >= 0)) or (not (3 > action.col >= 0)) or self.grid[action.row, action.col] != 0:
            raise InvalidAction(f"Invalid move! ({action.row}, {action.col}), {self.grid[action.row, action.col]}")

        # update grid
        self.grid[action.row][action.col] = action.player
        self.winner = self.check_winner()
        return self.winner

    def check_winner(self) -> int:
        grid = self.grid
        for i in range(3):
            # check rows
            if (grid[i, 0] != 0) and (grid[i, 0] == grid[i, 1]) and (grid[i, 0] == grid[i, 2]):
                return grid[i, 0]

            # check cols
            if (grid[0, i] != 0) and (grid[0, i] == grid[1, i]) and (grid[0][i] == grid[2][i]):
                return grid[0, i]

        # check diags
        if (grid[0, 0] != 0) and (grid[0, 0] == grid[1, 1]) and (grid[0, 0] == grid[2, 2]):
            return grid[0, 0]
        if (grid[2, 0] != 0) and (grid[2, 0] == grid[1, 1]) and (grid[2, 0] == grid[0][2]):
            return grid[2, 0]

        return 0

    def draw(self, shadow=False):
        a = self.grid
        winner = self.winner
        if winner == -1:
            return circle_big.copy()
        if winner == 1:
            return cross_big.copy()
        sb = small_board.copy()
        for i in range(3):
            for j in range(3):
                fig = None
                if a[i, j] == 1:
                    fig = cross_small
                if a[i, j] == -1:
                    fig = circle_small
                if fig is not None:
                    sb.paste(fig, (3 + 35 * j, 3 + 35 * i), fig)
        if shadow:
            alpha = sb.getchannel('A')
            new_alpha = alpha.point(lambda x: int(x * 187 / 255) if x > 0 else 0)
            sb.putalpha(new_alpha)
        return sb
