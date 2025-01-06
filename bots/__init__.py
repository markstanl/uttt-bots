import copy
from abc import ABC, abstractmethod
from typing import Any, Tuple, Set

from ultimate_tic_tac_toe.game import Game
from ultimate_tic_tac_toe import Move, Player, Outcome


class Bot(ABC):
    """
    Abstract base class for playable_bots.
    """

    @abstractmethod
    def update(self, game_state: Any) -> None:
        """
        Updates the bot's internal state based on the current game state.
        This method is called after every move in the game.

        Args:
            game_state (Any): The current state of the game, provided as input for decision-making.
                              The format of `game_state` should be defined by the game logic.
        """
        pass

    @abstractmethod
    def pick_move(self) -> Move:
        """
        Determines the bot's next move.

        Args:
            game_state (Any): The current state of the game, provided as input for decision-making.
                              The format of `game_state` should be defined by the game logic.

        Returns:
            Move: The bot's chosen move.
        """
        pass

    @abstractmethod
    def set_player(self, player: Player) -> None:
        """
        Sets the player as X or O
        """
        pass

    @abstractmethod
    def __name__(self):
        pass


class GameState:
    def __init__(self, game: Game):
        self.game = game

    def get_current_player(self) -> Player:
        return self.game.current_player

    def get_legal_moves(self) -> Set[Move]:
        return self.game.get_legal_moves()

    def make_move(self, move: Move) -> None:
        self.game.push(move)

    def get_bitboard(self) -> int:
        return self.game.bitboard

    def get_x_bitboard(self) -> int:
        return self.game.x_bitboard

    def get_o_bitboard(self) -> int:
        return self.game.o_bitboard

    def get_big_bitboard(self) -> int:
        return self.game.big_bitboard

    def get_x_big_bitboard(self) -> int:
        return self.game.x_big_bitboard

    def get_o_big_bitboard(self) -> int:
        return self.game.o_big_bitboard

    def get_next_board_index(self) -> int:
        return self.game.next_board_index

    def get_outcome(self) -> Outcome:
        return self.game.get_outcome()

    def is_game_over(self) -> bool:
        return self.game.is_game_over()

    def get_game(self) -> Game:
        return self.game

    def copy(self):
        return GameState(copy.copy(self.game))

    def push(self, move):
        self.game.push(move)

    def pop(self):
        self.game.pop()

    def __copy__(self):
        return GameState(copy.copy(self.game))

    def __str__(self):
        return str(self.game)

class Evaluation(ABC):
    @abstractmethod
    def evaluate(self, game_state: GameState) -> float:
        pass
