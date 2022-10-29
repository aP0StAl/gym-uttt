import random

import gym
import numpy as np
import pytest


@pytest.fixture(scope='module')
def env():
    env = gym.make('gym_uttt:Ultimate-Tic-Tac-Toe-v0')
    yield env
    env.close()


def test_init(env):
    assert env.game.current_player == 1


def test_reset(env):
    init_state, info = env.reset()
    for i in range(10):
        action = random.choice(info.get('valid_actions'))
        step_state, _, _, _, info = env.step(action)

    reset_state, _ = env.reset()
    np.testing.assert_array_equal(init_state, reset_state)
