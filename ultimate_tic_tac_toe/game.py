"""
Class for handling any and all game logic for an Ultimate Tic Tac Toe game,
optimized for use in a bot environment.
"""
import datetime
from typing import Optional

from ultimate_tic_tac_toe import Player, Move, Outcome, InvalidMoveError, \
    IllegalMoveError, WINNING_MASKS, Termination
from ultimate_tic_tac_toe.move_generator import generate_legal_moves


class Game:
    def __init__(self, event="Python UTTT",
                 site="N/A",
                 date=datetime.date.today(),
                 round="-",
                 x_player="Unnamed",
                 o_player="Unnamed",
                 annotator=None,
                 time=None,
                 time_control=None):
        self.number_to_letter_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E',
                                     5: 'F', 6: 'G', 7: 'H', 8: 'I'}
        self.letter_to_number_map = {v: k for k, v in
                                     self.number_to_letter_map.items()}

        # initialize the boards
        # these are "small" bitboards (as they represent the 9x9 small tiles)
        self.bitboard = 0
        self.x_bitboard = 0
        self.o_bitboard = 0
        # these are the "big" bitboards (as they represent the 3x3 big tiles)
        self.big_bitboard = 0
        self.x_big_bitboard = 0
        self.o_big_bitboard = 0

        self.next_board_index = 0
        self.made_moves = []
        self.current_player = Player.X

        # Metadata, for writing to UTTT
        self.event = event
        self.site = site
        self.date = date
        self.round = round
        self.x_player = x_player
        self.o_player = o_player
        self.annotator = annotator
        self.time = time
        self.time_control = time_control
        self.outcome = None

    def push(self, move: Move):
        if not isinstance(move, Move):
            raise InvalidMoveError(
                "Move must be an instance of the Move class.")

        # check for validity of move
        if not self.is_legal(move):
            if self.outcome is not None:
                raise IllegalMoveError(
                    f"Game is over. {self.outcome.result()}")
            raise IllegalMoveError(
                f"{move.__repr__()} is an llegal move. Current legal moves are: {str(generate_legal_moves(self.bitboard, self.big_bitboard, self.next_board_index, self.current_player))}")

        if move.player != self.current_player:
            raise IllegalMoveError("Wrong player.")

        # Update the bitboards
        self.bitboard |= 1 << move.index
        if move.player == Player.X:
            self.x_bitboard |= 1 << move.index
        else:
            self.o_bitboard |= 1 << move.index

        # Update the big board bitboard
        big_tile_index = move.index // 27 * 3 + move.index % 9 // 3
        current_player_bitboard = self.x_bitboard if move.player == Player.X else self.o_bitboard
        current_player_small_board = self.generate_small_board(
            current_player_bitboard, big_tile_index)

        if self.check_small_tic_tac_toe(current_player_small_board):
            # only need to check the tile the move was made in
            self.big_bitboard |= 1 << big_tile_index
            if move.player == Player.X:
                self.x_big_bitboard |= 1 << big_tile_index
                if self.check_tic_tac_toe(self.x_big_bitboard):
                    self.outcome = Outcome(Termination.TIC_TAC_TOE, Player.X)
                elif self.check_bitboard_is_full(self.big_bitboard):
                    self.outcome = Outcome(Termination.DRAW, None)

            else:
                self.o_big_bitboard |= 1 << big_tile_index
                if self.check_tic_tac_toe(self.o_big_bitboard):
                    self.outcome = Outcome(Termination.TIC_TAC_TOE, Player.O)
                elif self.check_bitboard_is_full(self.big_bitboard):
                    self.outcome = Outcome(Termination.DRAW, None)

        elif self.check_bitboard_is_full(
                self.generate_small_board(self.bitboard, big_tile_index)):
            # if the small board is full, update big bitboard so no nums
            # can be played in that tile
            self.big_bitboard |= 1 << big_tile_index
            if self.check_bitboard_is_full(self.big_bitboard):
                self.outcome = Outcome(Termination.DRAW, None)

        # update game information
        self.next_board_index = 1 << (
                move.index % 3 + 3 * (move.index // 9 % 3))
        if self.next_board_index & self.big_bitboard:
            self.next_board_index = 0

        self.current_player = Player.O if self.current_player == Player.X else Player.X
        self.made_moves.append(move)

    def pop(self) -> Move:
        """
        Pop the last move from the game.

        Returns:
            Move: The move that was popped.
        """
        # check for validity of move
        if not self.made_moves:
            raise ValueError("No moves to pop.")

        # pop the move from the list
        move = self.made_moves.pop()

        if self.outcome:
            self.outcome = None

        # Update the small bitboards
        self.bitboard &= ~(1 << move.index)
        if move.player == Player.X:
            self.x_bitboard &= ~(1 << move.index)
        else:
            self.o_bitboard &= ~(1 << move.index)

        # Update the big board
        old_tile_index = move.index // 27 * 3 + move.index % 9 // 3
        self.big_bitboard &= ~(1 << old_tile_index)
        if move.player == Player.X:
            self.x_big_bitboard &= ~(1 << old_tile_index)
        else:
            self.o_big_bitboard &= ~(1 << old_tile_index)

        # Update game information
        last_move = self.made_moves[-1] if self.made_moves else None
        self.next_board_index = 1 << (last_move.index % 3 + 3 * (
                last_move.index // 9 % 3)) if last_move else 0
        self.current_player = Player.O if self.current_player == Player.X else Player.X

        return move

    def check_tic_tac_toe(self, bitboard: int) -> bool:
        """
        Check if a player has won the given bitboard

        Args:
            bitboard (int): The 3x3 bitboard to check.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        return any((bitboard & mask) == mask for mask in WINNING_MASKS)

    def generate_small_board(self, bitboard: int,
                             small_board_index: int) -> int:
        """
        Generate a 3x3 small board from the 81-bit board and index of small board
        Args:
            bitboard: The 81-bit number representing a player's board.
            small_board_index: Index (0-8) of the small 3x3 board to generate.

        Returns:
            int: The 3x3 small board.
        """
        # Compute row and column offsets for the small board
        row_offset = (small_board_index // 3) * 3
        col_offset = (small_board_index % 3) * 3

        # creates a new 3x3 small board
        small_board = 0
        for row in range(3):
            for col in range(3):
                bit_index = (row_offset + row) * 9 + (col_offset + col)
                small_board |= ((bitboard >> bit_index) & 1) << (row * 3 + col)
        return small_board

    def check_small_tic_tac_toe(self, small_board: int) -> bool:
        """
        Check for a Tic Tac Toe win in a specific small board.

        Args:
            small_board (int): The 3x3 small board to check.

        Returns:
            bool: True if there's a Tic Tac Toe, False otherwise.
        """
        return self.check_tic_tac_toe(small_board)

    def check_bitboard_is_full(self, bitboard: int) -> bool:
        """
        Check if a small board is full.

        Args:
            bitboard (int): The small board to check if is full.

        Returns:
            bool: True if the small board is full, False otherwise.
        """
        return bitboard == 0b111_111_111

    def is_legal(self, move: Move) -> bool:
        """
        Check if a move is legal.

        Args:
            move (Move): The move to check.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        if self.outcome is not None:
            return False

        current_big_tile_index = move.index // 27 * 3 + move.index % 9 // 3
        if self.next_board_index and not (
                self.next_board_index & (1 << current_big_tile_index)):
            return False

        return not (self.bitboard & (1 << move.index))

    def outcome(self) -> Optional[Outcome]:
        return self.outcome

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.outcome is not None

    def get_legal_moves(self):
        return generate_legal_moves(self.bitboard,
                                    self.big_bitboard,
                                    self.next_board_index,
                                    self.current_player)

    def __str__(self):
        """
        Render the board as a human-readable string.
        """

        def render_bitboard(bitboard):
            """
            Converts a bitboard into a list of rows, with the first bit (rightmost)
            mapping to the bottom-left value.
            """
            rows = []
            for i in range(8, -1,
                           -1):  # Iterate from the bottom row (8) to the top row (0)
                row = ""
                for j in range(9):  # Iterate left to right within each row
                    # Calculate the bit position for the (i, j) cell
                    position = i * 9 + j
                    if bitboard & (1 << position):
                        row += str(Player.X)  # X occupies this position
                    elif self.o_bitboard & (1 << position):
                        row += str(Player.O)  # O occupies this position
                    else:
                        row += str(Player.EMPTY)
                rows.append(row)
            return rows

        board = render_bitboard(self.x_bitboard)
        result = ""
        for i in range(9):
            # Add a newline after every 3 rows for visual clarity
            if i % 3 == 0 and i != 0:
                result += "----+----+----\n"
            result += " | ".join(
                ["".join(board[i][j:j + 3]) for j in range(0, 9, 3)]) + "\n"

        return result.strip()

    def __copy__(self):
        new_board = Game(
            event=self.event,
            site=self.site,
            date=self.date,
            round=self.round,
            x_player=self.x_player,
            o_player=self.o_player,
            annotator=self.annotator,
            time=self.time,
            time_control=self.time_control,
        )

        new_board.bitboard = self.bitboard
        new_board.x_bitboard = self.x_bitboard
        new_board.o_bitboard = self.o_bitboard
        new_board.big_bitboard = self.big_bitboard
        new_board.x_big_bitboard = self.x_big_bitboard
        new_board.o_big_bitboard = self.o_big_bitboard
        new_board.next_board_index = self.next_board_index
        new_board.made_moves = list(self.made_moves)
        new_board.current_player = self.current_player
        new_board.outcome = self.outcome.copy() if self.outcome else None
        return new_board

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False

        attributes = [
            'bitboard', 'x_bitboard', 'o_bitboard', 'big_bitboard',
            'x_big_bitboard', 'o_big_bitboard', 'next_board_index',
            'made_moves', 'current_player', 'outcome'
        ]

        for attr in attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True


if __name__ == '__main__':
    move_1 = Move.from_algebraic("A1", Player.X)
    move_2 = Move.from_algebraic("B2", Player.O)
    move_3 = Move.from_algebraic("D4", Player.X)

    game = Game()
    game.push(move_1)
    print(game.bitboard)
    print(game)
    game.push(move_2)
    print(game)
    game.push(move_3)
    print(game)
