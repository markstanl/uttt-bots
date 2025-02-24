"""
Converts a UTTTAI bytearray into my UTTT game.
"""
from ultimate_tic_tac_toe import Player, Move, Termination, Outcome
from ultimate_tic_tac_toe.game import Game


def load_utttai(byte_array: bytearray):
    game = Game()

    subgame = byte_array[:80]
    supergame = byte_array[81:89]
    current_player = byte_array[90]
    constraint = byte_array[91]
    result = byte_array[90]

    for i, tile in enumerate(subgame):
        if tile == 1:
            game.force_push(Move(i, Player.X))
        if tile == 2:
            game.force_push(Move(i, Player.O))

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


def utttai_small_index_to_u3t_small_index(index: int):
    return index

def u3t_small_index_to_utttai_small_index(index: int):
    return index


def utttai_big_index_to_u3t_big_index(index: int):
    return 3 * (2 - (index // 3)) + index % 3

def u3t_big_index_to_utttai_big_index(index: int):
    return 3 * (2 - (index // 3)) + index % 3


def utttai_to_input_tensor(byte_array: bytearray):
    """
    Differs from the previous method by eliminating the need to initialize an
    entire game of U3T. Instead, it immediately generates the tensor to be
    used in the NN. Will speed up the process significantly.

    Args:
        byte_array:

    Returns:

    """
    pass