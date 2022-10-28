from gym.envs.registration import register

register(
    id='Ultimate-Tic-Tac-Toe-v0',
    entry_point='gym_uttt.envs:Uttt',
)
