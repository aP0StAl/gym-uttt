import os
from pathlib import Path
from typing import List, Optional

import numpy as np
from PIL import Image
from gym.error import InvalidAction

from gym_uttt.game.engine.action import Action
from gym_uttt.game.engine.tic_tac_toe_grid import TicTacToeGrid


p = Path(__file__).parents[2]
background = Image.open(
    os.path.join(p, 'assets/Background.jpg')
).transpose(Image.Transpose.ROTATE_90).crop((0, 0, 880, 1064))  # noqa Pycharm warning for Transpose
background.thumbnail((background.size[0] // 2, background.size[1] // 2))
logo_cg = Image.open(os.path.join(p, 'assets/logoCG.png'))
logo_cg.thumbnail((logo_cg.size[0] // 2, logo_cg.size[1] // 2))
logo = Image.open(os.path.join(p, 'assets/logo.png'))
logo.thumbnail((logo.size[0] // 2, logo.size[1] // 2))
board_border = Image.open(os.path.join(p, 'assets/board_border.png'))
board_border.thumbnail((board_border.size[0] // 2, board_border.size[1] // 2))
big_board = Image.open(os.path.join(p, 'assets/big_board.png'))
big_board.thumbnail((big_board.size[0] // 2, big_board.size[1] // 2))

y_ = 20
x_ = (background.size[0] - logo_cg.size[0])//2
background.paste(logo_cg, (x_, y_), logo_cg)
y_ += logo_cg.size[1] + 15

x_ = (background.size[0] - logo.size[0])//2
background.paste(logo, (x_, y_), logo)
y_ += logo.size[1] + 15


class TicTacToeGame:
    master_grid: TicTacToeGrid
    small_grids: List[List[TicTacToeGrid]]
    last_action: Optional[Action]
    current_player: int
    valid_actions: List[Action]

    def __init__(self):
        self.master_grid = TicTacToeGrid()
        self.small_grids = [[TicTacToeGrid() for _ in range(3)] for _ in range(3)]
        self.last_action = None
        self.current_player = 1
        self.valid_actions = self.get_valid_actions()
        self.shadow = [False] * 9

    def turn(self, action: Action) -> (bool, bool, bool):
        if action not in self.valid_actions:
            raise InvalidAction("Invalid move!")
        action.player = self.current_player
        self.last_action = action
        self.current_player = - self.current_player
        grid = self.small_grids[action.row // 3][action.col // 3]
        grid_winner = False
        game_winner = False
        done = False
        if grid.play(Action(action.row % 3, action.col % 3, action.player)) != 0:
            grid_winner = True
            if self.master_grid.play(Action(action.row // 3, action.col // 3, action.player)) != 0:
                game_winner = self.master_grid.winner
                done = True
        self.valid_actions = self.get_valid_actions()
        if not self.valid_actions:
            done = True
        return grid_winner, game_winner, done

    def get_state(self) -> np.array:
        state = np.zeros((9, 9), dtype='int8')
        for i in range(3):
            for j in range(3):
                g = self.small_grids[i][j]
                if g.winner:
                    state[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)] = np.ones((3, 3)) * g.winner
                else:
                    state[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)] = g.grid
        return state.reshape(-1)

    def get_valid_actions(self) -> List[Action]:
        valid_actions = []
        self.shadow = [True] * 9
        if self.last_action is not None:
            last_action = self.last_action
            grid = self.small_grids[last_action.row % 3][last_action.col % 3]
            for action in grid.get_valid_actions():
                a_row = (last_action.row % 3) * 3 + action.row
                a_col = (last_action.col % 3) * 3 + action.col
                valid_actions.append(Action(a_row, a_col, None))
            if valid_actions:
                self.shadow[3 * (last_action.row % 3) + (last_action.col % 3)] = False
        if not valid_actions:
            for row in range(3):
                for col in range(3):
                    grid = self.small_grids[row][col]
                    for action in grid.get_valid_actions():
                        self.shadow[3 * row + col] = False
                        a_row = (row % 3) * 3 + action.row
                        a_col = (col % 3) * 3 + action.col
                        valid_actions.append(Action(a_row, a_col, None))
        return valid_actions

    def draw(self):
        bg = background.copy()
        bb = board_border.copy()
        bb.paste(big_board, (20, 20), big_board)
        for i in range(3):
            for j in range(3):
                sb = self.small_grids[i][j].draw(shadow=self.shadow[3*i+j])
                bb.paste(sb, (20 + j * 130, 20 + i * 130), sb)
        x = (background.size[0] - bb.size[0]) // 2
        y = y_
        bg.paste(bb, (x, y), bb)
        return bg
