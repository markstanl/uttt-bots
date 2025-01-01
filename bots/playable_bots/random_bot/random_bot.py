import random
from abc import ABC
from typing import Any, Tuple
from ultimate_tic_tac_toe import Move
from bots import Bot, GameState


class RandomBot(Bot, ABC):
    def __init__(self, bot_name: str = "random_bot"):
        self.player = None
        self.game_state = None
        self.bot_name = bot_name

    def set_player(self, player: str) -> None:
        self.player = player

    def pick_move(self) -> Move:
        if self.game_state.is_game_over():
            raise ValueError('Game is over')

        if self.game_state.get_current_player() != self.player:
            raise ValueError('Not the bot\'s turn')

        valid_moves = self.game_state.get_legal_moves()
        return random.choice(list(valid_moves))

    def update(self, game_state: GameState) -> None:
        self.game_state = game_state

    def __name__(self):
        return self.bot_name
