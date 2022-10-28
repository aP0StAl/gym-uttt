import gym
import pytest


@pytest.fixture(scope='module')
def env():
    env = gym.make('gym_uttt:Ultimate-Tic-Tac-Toe-v0')
    yield env
    env.close()


def test_init(env):
    assert env.game.current_player == 1
