from abc import ABC, abstractmethod
from typing import Any, Tuple
from game.ultimate_tic_tac_toe import UltimateTicTacToe


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
    def pick_move(self) -> Tuple[int, int]:
        """
        Determines the bot's next move.

        Args:
            game_state (Any): The current state of the game, provided as input for decision-making.
                              The format of `game_state` should be defined by the game logic.

        Returns:
            Tuple[int, int]: The chosen move as a tuple (row, column) or any other format
                             your game logic requires.
        """
        pass

    @abstractmethod
    def set_player(self, player: str) -> None:
        """
        Sets the player as X or O
        """
        pass

    @abstractmethod
    def __name__(self):
        pass


class GameState:
    def __init__(self, game: UltimateTicTacToe):
        self.game = game

    def get_current_player(self):
        return self.game.current_player

    def get_valid_moves(self):
        return self.game.get_valid_moves(False)

    def get_board(self):
        return self.game.board

    def get_next_board_coordinates(self):
        return self.game.next_board_coordinates

    def get_winner(self):
        return self.game.winner

    def is_game_over(self):
        return self.game.game_over
