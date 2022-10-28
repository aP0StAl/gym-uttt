from typing import List, Optional

import numpy as np
from gym.error import InvalidAction

from gym_uttt.game.engine.action import Action
from gym_uttt.game.engine.tic_tac_toe_grid import TicTacToeGrid


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
        if grid.play(Action(action.row % 3, action.col % 3, action.player)) > 0:
            grid_winner = True
            if self.master_grid.play(Action(action.row // 3, action.col // 3, action.player)) > 0:
                game_winner = True
                done = True
        self.valid_actions = self.get_valid_actions()
        if not self.valid_actions:
            done = True
        return grid_winner, game_winner, done

    def get_state(self) -> np.array:
        state = np.array((9, 9))
        for i in range(3):
            for j in range(3):
                state[3*i:3*(i+1), 3*j:3*(j+1)] = self.small_grids[i][j]
        return state.reshape(-1)

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
