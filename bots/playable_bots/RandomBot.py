import random
from abc import ABC
from typing import Any, Tuple

from bots.Bot import Bot, GameState


class RandomBot(Bot, ABC):
    def __init__(self):
        self.player = None
        self.game_state = None

    def set_player(self, player: str) -> None:
        self.player = player

    def pick_move(self) -> Tuple[int, int]:
        if self.game_state.is_game_over():
            raise ValueError('Game is over')

        if self.game_state.get_current_player() != self.player:
            raise ValueError('Not the bot\'s turn')

        valid_moves = self.game_state.get_valid_moves()
        return random.choice(valid_moves)

    def update(self, game_state: GameState) -> None:
        self.game_state = game_state

    def __name__(self):
        return "RandoTron"
