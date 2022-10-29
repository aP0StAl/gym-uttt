from typing import Optional, Union, List, Tuple

import gym
import numpy as np
from gym.core import RenderFrame, ActType, ObsType

from gym_uttt.game.engine.action import Action
from gym_uttt.game.engine.gamelogic import TicTacToeGame


class Uttt(gym.Env):
    """
    Description:
        Ultimate Tic-Tac-Toe game environment

    Observation:
        Type: Box(9, 9)

    Actions:
        Type: Box(2)

    Reward:
        10 for final winner
        3 for draw
        1 for winner on small board
    """

    def __init__(self):
        self.game = TicTacToeGame()
        self.action_space = gym.spaces.Box(0, 8, shape=(2,), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(-1, 1, shape=(81,), dtype=np.int8)

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        grid_winner, game_winner, done = self.game.turn(Action(action[0], action[1], None))
        reward = 0
        if grid_winner:
            reward = 1
        if done:
            reward = 3
        if game_winner:
            reward = 10
        game_state = self.game.get_state()
        return game_state, reward, done, False, {"valid_actions": self.get_valid_actions()}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ) -> Tuple[ObsType, dict]:
        self.game = TicTacToeGame()
        game_state = self.game.get_state()
        return game_state, {"valid_actions": self.get_valid_actions()}

    def get_valid_actions(self):
        return [(x.row, x.col) for x in self.game.valid_actions]

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        pass
