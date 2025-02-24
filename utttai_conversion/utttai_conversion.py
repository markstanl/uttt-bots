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
    big_row = index // 27
    big_col = index // 9 % 3
    print(big_row, big_col)

    return index

def u3t_small_index_to_utttai_small_index(index: int):
    """
    Converts a U3T small index to a UTTTAI small index.

    Args:
        index: The U3T small index.

    Returns:
        The UTTTAI small index.
    """
    return 60 - 27 * ((index // 9) // 3) - 3 * ((index // 9) % 3) + 9 * ((index % 9) // 3) + (index % 9) % 3



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

if __name__ == '__main__':
    u3t_to_utttai_small_pairs = [(0, 60), (1, 61), (2, 62), (3, 69),
                                      (4, 70), (5, 71), (6, 78), (7, 79),
                                      (8, 80),
                                      (9, 57), (10, 58), (11, 59), (12, 66),
                                      (13, 67), (14, 68), (15, 75), (16, 76),
                                      (17, 77),
                                      (18, 54), (19, 55), (20, 56), (21, 63),
                                      (22, 64), (23, 65), (24, 72), (25, 73),
                                      (26, 74),
                                      (27, 33), (28, 34), (29, 35), (30, 42),
                                      (31, 43), (32, 44), (33, 51), (34, 52),
                                      (35, 53),
                                      (36, 30), (37, 31), (38, 32), (39, 39),
                                      (40, 40), (41, 41), (42, 48), (43, 49),
                                      (44, 50),
                                      (45, 27), (46, 28), (47, 29), (48, 36),
                                      (49, 37), (50, 38), (51, 45), (52, 46),
                                      (53, 47),
                                      (54, 6), (55, 7), (56, 8), (57, 15),
                                      (58, 16), (59, 17), (60, 24), (61, 25),
                                      (62, 26),
                                      (63, 3), (64, 4), (65, 5), (66, 12),
                                      (67, 13), (68, 14), (69, 21), (70, 22),
                                      (71, 23),
                                      (72, 0), (73, 1), (74, 2), (75, 9),
                                      (76, 10), (77, 11), (78, 18), (79, 19),
                                      (80, 20)]
    updated_pairs = sorted(
        [(pair[1], pair[0]) for pair in u3t_to_utttai_small_pairs],
        key=lambda x: x[0])

    for pair in updated_pairs:
        print(pair)
        print(utttai_small_index_to_u3t_small_index(pair[0]), pair[1])
        print()