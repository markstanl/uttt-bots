"""
Class for handling any and all game logic for an Ultimate Tic Tac Toe game,
optimized for use in a bot environment.
"""
from typing import Optional
import datetime

from ultimate_tic_tac_toe import Player, Move, Outcome, InvalidMoveError, \
    IllegalMoveError, WINNING_MASKS, Termination
from ultimate_tic_tac_toe.move_generator import generate_legal_moves


class BotUltimateTicTacToe:
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
        self.valid_moves = []
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
        # check for validity of move
        if not self.is_legal(move):
            raise IllegalMoveError(f"{move.__repr__()} is an llegal move. Current legal moves are: {str(self.valid_moves)}")

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
        if self.check_small_tic_tac_toe(self.bitboard, move.index // 27 * 3 + move.index % 9 // 3):
            # only need to check the tile the move was made in
            self.big_bitboard |= 1 << big_tile_index
            if move.player == Player.X:
                self.x_big_bitboard |= 1 << big_tile_index
                if self.check_tic_tac_toe(self.x_big_bitboard):
                    self.outcome = Outcome(Termination.TIC_TAC_TOE, Player.X)

            else:
                self.o_big_bitboard |= 1 << big_tile_index
                if self.check_tic_tac_toe(self.o_big_bitboard):
                    self.outcome = Outcome(Termination.TIC_TAC_TOE, Player.O)

        # update game information
        self.next_board_index = 1 << (
                move.index % 3 + 3 * (move.index // 9 % 3))
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

        if self.outcome.termination == Termination.TIC_TAC_TOE:
            self.outcome = None

        # Update the small bitboards
        self.bitboard &= ~(1 << move.index)
        if move.player == Player.X:
            self.x_bitboard &= ~(1 << move.index)
        else:
            self.o_bitboard &= ~(1 << move.index)

        # Update the big board
        old_tile_index = move.index // 27 * 3 + move.index % 9 // 3
        self.big_bitboard &= ~(1 << move.index)
        if not self.check_small_tic_tac_toe(self.bitboard, old_tile_index):
            # if there isn't a ttt in small board, update the big board
            # boolean check may be unnecessary, consider this when refactoring
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

    def check_small_tic_tac_toe(self, bitboard: int, small_board_index: int) -> bool:
        """
        Check for a Tic Tac Toe win in a specific small board.

        Args:
            bitboard (int): The 81-bit number representing a player's board.
            small_board_index (int): Index (0-8) of the small 3x3 board to check.

        Returns:
            bool: True if there's a Tic Tac Toe, False otherwise.
        """
        # Compute row and column offsets for the small board
        row_offset = ( small_board_index // 3) * 3
        col_offset = (small_board_index % 3) * 3

        # creates a new 3x3 small board
        small_board = 0
        for row in range(3):
            for col in range(3):
                bit_index = (row_offset + row) * 9 + (col_offset + col)
                small_board |= ((bitboard >> bit_index) & 1) << (row * 3 + col)

        return self.check_tic_tac_toe(small_board)

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

        self.valid_moves = generate_legal_moves(self.bitboard,
                                                self.big_bitboard,
                                                self.next_board_index,
                                                self.current_player)
        return move in self.valid_moves

    def outcome(self) -> Optional[Outcome]:
        pass

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


if __name__ == '__main__':
    move_1 = Move.from_algebraic("A1", Player.X)
    move_2 = Move.from_algebraic("B2", Player.O)
    move_3 = Move.from_algebraic("D4", Player.X)

    game = BotUltimateTicTacToe()
    game.push(move_1)
    print(game.bitboard)
    print(game)
    game.push(move_2)
    print(game)
    game.push(move_3)
    print(game)
