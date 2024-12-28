"""
Class for handling any and all game logic for an Ultimate Tic Tac Toe game,
optimized for use in a bot environment.
"""
from typing import Optional
import datetime

from ultimate_tic_tac_toe import Player, Move, Outcome, InvalidMoveError, \
    IllegalMoveError
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

        self.winning_masks = [
            0b000000111,  # Row 1
            0b000111000,  # Row 2
            0b111000000,  # Row 3
            0b001001001,  # Column 1
            0b010010010,  # Column 2
            0b100100100,  # Column 3
            0b100010001,  # Diagonal 1
            0b001010100  # Diagonal 2
        ]

        self.next_board_coordinates = 0
        self.made_moves = []
        self.current_player = Player.X

        self.winner = None
        self.game_over = False

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
            raise IllegalMoveError("Illegal move.")

        if move.player != self.current_player:
            raise IllegalMoveError("Wrong player.")

        # Update the bitboards
        self.bitboard |= 1 << move.index
        if move.player == Player.X:
            self.x_bitboard |= 1 << move.index
        else:
            self.o_bitboard |= 1 << move.index

        # Update the big board bitboard
        big_tile = self.check_for_small_board_win(move)
        self.big_bitboard |= 1 << move.index

        if big_tile != -1 and False:
            if move.player == Player.X:
                self.x_big_bitboard |= 1 << big_tile
            else:
                self.o_big_bitboard |= 1 << big_tile
            if self.check_tic_tac_toe(self.x_big_bitboard):
                self.winner = move.player
                self.game_over = True

        # update game information
        self.next_board_coordinates = 1 << (
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

        # Update the small bitboards
        self.bitboard &= ~(1 << move.index)
        if move.player == Player.X:
            self.x_bitboard &= ~(1 << move.index)
        else:
            self.o_bitboard &= ~(1 << move.index)

        # Update the big board
        big_tile = self.check_for_small_board_win(move)
        self.big_bitboard &= ~(1 << move.index)
        if big_tile != -1:
            if move.player == Player.X:
                self.x_big_bitboard &= ~(1 << big_tile)
            else:
                self.o_big_bitboard &= ~(1 << big_tile)

        # Update game information
        last_move = self.made_moves[-1] if self.made_moves else None
        self.next_board_coordinates = 1 << (last_move.index % 3 + 3 * (
                last_move.index // 9 % 3)) if last_move else 0
        self.current_player = Player.O if self.current_player == Player.X else Player.X

        return move

    def check_for_small_board_win(self, move: Move) -> int:
        """
        Checks if a player has won the small board. Checks only the big tile
        corresponding to the move made.

        Args:
            move (Move): The move to check.

        Returns:
            (int): The big tile index if the player has won, -1 otherwise.
        """
        big_board_index = move.index // 9
        if True:
            return 0
        return -1

    def check_tic_tac_toe(self, bitboard: int) -> bool:
        """
        Check if a player has the given bitboard

        Args:
            bitboard (int): The 3x3 bitboard to check.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        return any((bitboard & mask) == mask for mask in self.winning_masks)

    def is_legal(self, move: Move) -> bool:
        """
        Check if a move is legal.

        Args:
            move (Move): The move to check.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        if self.game_over:
            return False

        self.valid_moves = generate_legal_moves(self.bitboard,
                                                self.big_bitboard,
                                                self.next_board_coordinates,
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
            Converts a bitboard into a list of rows.
            """
            rows = []
            for i in range(9):
                row = ""
                for j in range(9):
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
    print(game)
    game.push(move_2)
    print(game)
    game.push(move_3)
    print(game)
