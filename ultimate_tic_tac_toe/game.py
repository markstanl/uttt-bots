"""
Class for handling any and all game logic for an Ultimate Tic Tac Toe game,
optimized for use in a bot environment.
"""
import datetime
from typing import Optional

from ultimate_tic_tac_toe import Player, Move, Outcome, InvalidMoveError, \
    IllegalMoveError, WINNING_MASKS, SMALL_BITBOARD_WINNING_MASKS, \
    SMALL_BITBOARD_FULL_TILE_MASK, Termination, render_bitboard
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

        if self.check_small_tic_tac_toe(current_player_bitboard,
                                        big_tile_index):
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

        elif self.check_small_bitboard_is_full(self.bitboard, big_tile_index):
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

    def check_small_tic_tac_toe(self, player_bitboard: int,
                                big_tile_index: int) -> bool:
        """
        Check for a Tic Tac Toe win in a specific small board.

        Args:
            player_bitboard (int): The player's bitboard.
            small_tile_index (int): The index of the small tile to check.

        Returns:
            bool: True if there's a Tic Tac Toe, False otherwise.
        """
        left_transform_number = big_tile_index % 3 * 3 + (big_tile_index // 3 * 27)
        transformed_masks = [mask << left_transform_number for mask in SMALL_BITBOARD_WINNING_MASKS]
        return any((player_bitboard & mask) == mask for mask in transformed_masks)

    def check_small_bitboard_is_full(self, bitboard: int,
                               big_tile_index: int) -> bool:
        """
        Check if a small board is full.

        Args:
            bitboard (int): Big bitboard to check
            big_tile_index (int): Index of the big tile to check

        Returns:
            bool: True if the small board is full, False otherwise.
        """
        left_transform_number = big_tile_index % 3 * 3 + (big_tile_index // 3 * 27)
        return (bitboard & (
                    SMALL_BITBOARD_FULL_TILE_MASK << left_transform_number)) == (
                SMALL_BITBOARD_FULL_TILE_MASK << left_transform_number)

    def force_push(self, move: Move):
        """
        Force a move onto the board without checking for legality.
        Args:
            move: The move to force onto the board.
        """
        if not isinstance(move, Move):
            raise InvalidMoveError(
                "Move must be an instance of the Move class.")

        # Update the bitboards
        self.bitboard |= 1 << move.index
        if move.player == Player.X:
            self.x_bitboard |= 1 << move.index
        else:
            self.o_bitboard |= 1 << move.index

        # Update the big board bitboard
        big_tile_index = move.index // 27 * 3 + move.index % 9 // 3
        current_player_bitboard = self.x_bitboard if move.player == Player.X else self.o_bitboard

        if self.check_small_tic_tac_toe(current_player_bitboard,
                                        big_tile_index):
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

        elif self.check_small_bitboard_is_full(self.bitboard, big_tile_index):
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

    def update_current_player(self) -> str:
        """
        Only to be called if you run force_push on the game, and want to
        update the current player to what the next player should be.

        Returns:
            str: A description of what our best guess is
        """
        x_count = bin(self.x_bitboard).count('1')
        o_count = bin(self.o_bitboard).count('1')
        if x_count == o_count:
            self.current_player = Player.X
            return "X is the next player"
        elif x_count - 1 == o_count:
            self.current_player = Player.O
            return "O is the next player"
        elif x_count > o_count:
            self.current_player = Player.O
            return "O is probably the next player. Though the board seems is invalid"
        else:
            self.current_player = Player.X
            return "X is probably the next player. Though the board seems is invalid"

    def check_bitboard_is_full(self, bitboard: int) -> bool:
        """
        Check if a big board is full.

        Args:
            bitboard (int): The big bitboard to check.

        Returns:
            bool: True if the big board is full, False otherwise.
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

    def get_annotated_board(self) -> str:
        """
        Get the board as a string with annotations for each cell. Differs from
        the string by including extra information about each cell. As well as
        making big tiles that are won display the winning player's symbol.

        Returns:
            str: The annotated board.
        """
        winning_x_tile = ['X  X', ' X ', 'X X']
        winning_o_tile = [' O ', 'O O', ' O ']

        annotated_board = "  ABC DEF GHI\n"
        board = render_bitboard(self.bitboard, self.o_bitboard)
        i = 9
        for row in board:
            possible_index = (i - 1) * 9

            annotated_board += f"{i} "
            for j, space in enumerate(row):
                current_index = possible_index + j
                if self.x_big_bitboard & 1 << (current_index // 27 * 3 + current_index % 9 // 3) == 1:
                    annotated_board += winning_o_tile[i % 3 - 1][j % 3]
                elif self.o_big_bitboard & 1 << (current_index // 27 * 3 + current_index % 9 // 3) == 1:
                    annotated_board += winning_o_tile[i % 3 - 1][j % 3]
                else:
                    annotated_board += space
                if j % 3 == 2 and j != 8:
                    annotated_board += "|"

            if i % 3 == 1 and i != 1:
                annotated_board += "\n ----+---+----"
            annotated_board += "\n"
            i -= 1
        return annotated_board


    def __str__(self):
        """
        Render the board as a human-readable string.
        """
        board = render_bitboard(self.bitboard, self.o_bitboard)
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

        print(self.next_board_index, other.next_board_index)

        for attr in attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True


if __name__ == '__main__':
    move_1 = Move.from_algebraic("A1", Player.X)
    move_2 = Move.from_algebraic("B2", Player.O)
    move_3 = Move.from_algebraic("D4", Player.X)
    move_4 = Move.from_algebraic("C2", Player.O)
    move_5 = Move.from_algebraic("G4", Player.X)
    move_6 = Move.from_algebraic("A2", Player.O)
    move_7 = Move.from_algebraic("A4", Player.X)

    game = Game()
    game.push(move_1)
    game.push(move_2)
    game.push(move_3)
    game.push(move_4)
    game.push(move_5)
    game.push(move_6)
    game.push(move_7)
    print(game.get_legal_moves())
    print(game.get_annotated_board())
