"""
Converts a UTTTAI bytearray into my UTTT game. The most notable methods here
are the load_utttai and byteboard_refactor methods. The load_utttai method
converts a UTTTAI bytearray into a UTTT game. The byteboard_refactor method
converts a UTTTAI bytearray into a more standard format, to be used as the
standard data in the huggingface dataset. The other methods are helpers
"""
from ultimate_tic_tac_toe import Player, Move, Termination, Outcome
from ultimate_tic_tac_toe.game import Game
from utttai_conversion import utttai_to_u3t_dict


def load_utttai(byte_array: bytearray):
    """
    Converts a UTTTAI bytearray into a UTTT game.

    Args:
        byte_array: the UTTTAI bytearray

    Returns:
        the UTTT game
    """
    game = Game()

    subgame = byte_array[:80]
    supergame = byte_array[81:89]
    current_player = byte_array[90]
    constraint = byte_array[91]
    result = byte_array[90]

    for i, tile in enumerate(subgame):
        if tile == 1:
            game.force_push(Move(utttai_to_u3t[i], Player.X))
        if tile == 2:
            game.force_push(Move(utttai_to_u3t[i], Player.O))

    for i, big_tile in enumerate(supergame):
        if big_tile == 1:
            game.big_bitboard = game.big_bitboard & 1 << i
            game.x_big_bitboard = game.big_bitboard & 1 << i
        if big_tile == 2:
            game.big_bitboard = game.big_bitboard & 1 << i
            game.o_big_bitboard = game.big_bitboard & 1 << i

    game.current_player = Player.X if current_player == 1 else Player.O
    game.next_board_index = 0 if constraint == 't'.encode(
        'utf-8') else constraint + 1

    if result != 0:
        if result == 3:
            game.outcome = Outcome(Termination.DRAW, None)
        else:
            game.outcome = Outcome(Termination.TIC_TAC_TOE,
                                   Player.X if result == 1 else Player.O)

    return game


def utttai_to_u3t(index: int):
    """
    Converts a UTTTAI small index to a U3T small index.

    Args:
        index: the original utttai index


    Returns:
        the updated u3t index
    """
    return 27 * (2 - (index // 27)) + 9 * (2 - ((index // 3) % 3)) + (
                index % 3) + 3 * ((index // 9) % 3)


def u3t_to_utttai(index: int):
    """
    Converts a U3T small index to a UTTTAI small index.

    Args:
        index: The U3T small index.

    Returns:
        The UTTTAI small index.
    """
    return 60 - 27 * ((index // 9) // 3) - 3 * ((index // 9) % 3) + 9 * (
                (index % 9) // 3) + (index % 9) % 3


def utttai_to_u3t_big(index: int):
    """
    Converts a UTTTAI big index to a U3T big index.
    """
    return 3 * (2 - (index // 3)) + index % 3


def u3t_to_utttai_big(index: int):
    """
    Converts a UTTTAI big index to a U3T big index.
    Same method crazzzyy
    """
    return 3 * (2 - (index // 3)) + index % 3


def byteboard_refactor(board: bytearray) -> bytearray:
    """
    Converts a UTTTAI bytearray into a more standard format. Consider the
    original format of the byte array

    byte_array = / "subgames" (small board) / "supergames" (big board)
                    (81 bytes)                  (9 bytes)
                    / current player / constraint /  result
                        (1 byte)       (1 byte)    (1 byte)

    The subgames are 81 bytes long, but use the weird UTTTAI indexing system,
    we will switch that to a more standard 81 byte array. The supergames are
    indexed backwards, which is a pretty easy fix. The current player,
    constraint, and result will remain unchanged


    Args:
        board: the original byte array

    Returns:
        the updated byte array
    """
    if len(board) != 93:
        raise ValueError("The byte array must be 93 bytes long")

    converted_board = board.copy()

    for i in range(81):
        converted_board[80 - utttai_to_u3t_dict[i]] = board[i]

    for i in range(9):
        converted_board[89 - utttai_to_u3t_big(i)] = board[81 + i]

    if board[91] != 9:
        converted_board[91] = utttai_to_u3t_big(board[91])

    return converted_board

def numerical_string_refactor(board: int or str, return_type: str = 'int') -> int or str:
    """
    Performs the same conversion as the byteboard_refactor method, but on a
    numerical string. This is used for the hugging face dataset

    Args:
        board: the original board

    Returns:
        the updated board
    """
    if len(str(board)) != 93:
        raise ValueError("The board must be 93 bytes long")

    if(type(board) == int):
        board = str(board)

    converted_board = [0] * 93

    for i in range(81):
        converted_board[80 - utttai_to_u3t_dict[int(i)]] = int(board[int(i)])

    for i in range(9):
        converted_board[89 - utttai_to_u3t_big(int(i))] = int(board[81 + int(i)])

    converted_board[90] = int(board[90])

    if int(board[91]) != 9:
        converted_board[91] = utttai_to_u3t_big(int(board[91]))
    else:
        converted_board[91] = 9
    converted_board[92] = int(board[92])

    if return_type == 'str':
        return ''.join([str(i) for i in converted_board])

    return array_to_int(converted_board)

def array_to_int(array_like: bytearray or list) -> int:
    """
    Converts a byte array to an int

    Args:
        byte_array: the byte array

    Returns:
        the int
    """
    i = 0
    num = 0
    for val in reversed(array_like):
        num += int(val) * (10 ** i)
        i += 1
    return num