from bots import Bot, Evaluation
from ultimate_tic_tac_toe import Player


class Minimax2(Bot):
    def __init__(self, evaluation: Evaluation, player: Player,
                 bot_name: str = "minimax_2"):
        self.evaluation = evaluation
        self.player = player
