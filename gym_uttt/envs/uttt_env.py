from typing import Optional, Union, List, Tuple

import gym
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
        return game_state, reward, done, False, {}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ) -> Tuple[ObsType, dict]:
        self.game = TicTacToeGame()
        game_state = self.game.get_state()
        return game_state, {}

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        pass
