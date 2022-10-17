from typing import Optional, Union, List, Tuple

import gym
from gym.core import RenderFrame, ActType, ObsType


class Uttt(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        pass

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        pass
