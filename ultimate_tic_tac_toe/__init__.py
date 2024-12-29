"""
Much of this file is copied and altered from the `pythin-chess` library, which
is licensed under the GNU License.
"""
import dataclasses
from enum import Enum, auto
from typing import Optional, TypeAlias, List
import re

FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

RANK_NAMES = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


class Player(Enum):
    """
    Enum for representing a player in Ultimate Tic Tac Toe.
    """
    X = 'X'
    O = 'O'
    EMPTY = '_'

    def __str__(self):
        return self.value


class Move:
    def __init__(self, index: int, player: Player):
        """
        Initialize a move for Ultimate Tic Tac Toe.

        Args:
            index (int): Bitboard index (0-80) representing the position.
            player (Player): The player making the move ('X' or 'O').
        """
        if player == Player.EMPTY:
            raise ValueError("Player cannot be empty.")

        self.index = index
        self.player = player

    def __str__(self):
        """
        String representation of the move.

        Returns:
            str: A human-readable representation of the move.
        """
        row = self.index // 9
        col = self.index % 9
        return f"Player {self.player} on index {self.index}, ({self.to_algebraic()})"

    def __repr__(self):
        """
        String representation of the move.

        Returns:
            str: Algebraic notation of the move.
        """
        return f"{self.to_algebraic()} {str(self.player)}"

    @classmethod
    def from_algebraic(cls, notation: str, player: Player):
        """
        Create a Move from algebraic notation.

        Args:
            notation (str): Algebraic notation like 'B2'.
            player (Player): The player making the move.

        Returns:
            Move: A new Move instance.
        """
        if player == Player.EMPTY:
            raise ValueError("Player cannot be empty.")

        notation = notation.lower()

        if not re.match(r"^[a-i][1-9]$", notation):
            raise ValueError("Invalid algebraic notation.")

        return cls(parse_square(notation), player)

    @classmethod
    def from_bitboard(cls, binary_num, player: Player):
        """
        Create a Move from a single bitboard index (0-80).

        Args:
            binary_num (int): A bitboard index (0-80).
            player (Player): The player making the move

        Returns:
            Move: A new Move instance.
        """
        if player == Player.EMPTY:
            raise ValueError("Player cannot be empty.")

        return cls((binary_num & -binary_num).bit_length() - 1, player)

    def to_algebraic(self):
        """
        Convert the move to algebraic notation.

        Returns:
            str: Algebraic notation like 'b2'.
        """
        return square_name(self.index)

    def to_binary(self):
        """
        Convert the move to binary notation.

        Returns:
            int: Binary notation like 0b000000001.
        """
        return 1 << self.index

    def __eq__(self, other):
        """
        Check if two moves are equal.
        """
        return self.index == other.index and self.player == other.player

    def __hash__(self) -> int:
        """
        Hash the move.
        """
        return hash((self.index, self.player))


class Termination(Enum):
    """
    Enum for representing the game termination state.
    """
    TIC_TAC_TOE = auto()
    DRAW = auto()

@dataclasses.dataclass
class Outcome:
    termination: Termination
    winner: Optional[Player]

    def result(self) -> str:
        """Returns ``1-0``, ``0-1`` or ``1/2-1/2``."""
        return "1/2-1/2" if self.winner is None else (
            "1-0" if self.winner else "0-1")


class InvalidMoveError(ValueError):
    """Raised when move notation is not syntactically valid"""


class IllegalMoveError(ValueError):
    """Raised when the attempted move is illegal in the current position"""


Square: TypeAlias = int
A1: Square = 0
B1: Square = 1
C1: Square = 2
D1: Square = 3
E1: Square = 4
F1: Square = 5
G1: Square = 6
H1: Square = 7
I1: Square = 8
A2: Square = 9
B2: Square = 10
C2: Square = 11
D2: Square = 12
E2: Square = 13
F2: Square = 14
G2: Square = 15
H2: Square = 16
I2: Square = 17
A3: Square = 18
B3: Square = 19
C3: Square = 20
D3: Square = 21
E3: Square = 22
F3: Square = 23
G3: Square = 24
H3: Square = 25
I3: Square = 26
A4: Square = 27
B4: Square = 28
C4: Square = 29
D4: Square = 30
E4: Square = 31
F4: Square = 32
G4: Square = 33
H4: Square = 34
I4: Square = 35
A5: Square = 36
B5: Square = 37
C5: Square = 38
D5: Square = 39
E5: Square = 40
F5: Square = 41
G5: Square = 42
H5: Square = 43
I5: Square = 44
A6: Square = 45
B6: Square = 46
C6: Square = 47
D6: Square = 48
E6: Square = 49
F6: Square = 50
G6: Square = 51
H6: Square = 52
I6: Square = 53
A7: Square = 54
B7: Square = 55
C7: Square = 56
D7: Square = 57
E7: Square = 58
F7: Square = 59
G7: Square = 60
H7: Square = 61
I7: Square = 62
A8: Square = 63
B8: Square = 64
C8: Square = 65
D8: Square = 66
E8: Square = 67
F8: Square = 68
G8: Square = 69
H8: Square = 70
I8: Square = 71
A9: Square = 72
B9: Square = 73
C9: Square = 74
D9: Square = 75
E9: Square = 76
F9: Square = 77
G9: Square = 78
H9: Square = 79
I9: Square = 80
Squares: List[Square] = list(range(81))

SQUARE_NAMES = [f + r for r in RANK_NAMES for f in FILE_NAMES]
print(SQUARE_NAMES)

WINNING_MASKS = [
    0b000000111,  # Row 1
    0b000111000,  # Row 2
    0b111000000,  # Row 3
    0b001001001,  # Column 1
    0b010010010,  # Column 2
    0b100100100,  # Column 3
    0b100010001,  # Diagonal 1
    0b001010100  # Diagonal 2
]


def parse_square(name: str) -> Square:
    """
    Gets the square index for the given square *name*
    (e.g., ``a1`` returns ``0``).

    :raises: :exc:`ValueError` if the square name is invalid.
    """
    return SQUARE_NAMES.index(name)


def square_name(square: Square) -> str:
    """Gets the name of the square, like ``a3``."""
    return SQUARE_NAMES[square]


def square(file_index: int, rank_index: int) -> Square:
    """Gets a square number by file and rank index."""
    return rank_index * 8 + file_index


def square_file(square: Square) -> int:
    """Gets the file index of the square where ``0`` is the a-file."""
    return square & 7


def square_rank(square: Square) -> int:
    """Gets the rank index of the square where ``0`` is the first rank."""
    return square >> 3
