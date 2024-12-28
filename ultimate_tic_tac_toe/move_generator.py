from typing import Set, Tuple
from ultimate_tic_tac_toe import Player, Move


def generate_legal_moves(bitboard: int,
                         big_bitboard: int,
                         next_tile: int,
                         player: Player) -> Set[Move]:
    """
    Generate a list of legal moves for the next player.

    Args:
        bitboard (int): The 3x3 bitboard.
        big_bitboard (int): The larger 3x3 grid for sections.
        next_tile ((int, int)): The row and column indices of the next tile.
        player (Player): The player making the move.

    Returns:
        Set[Move]: A list of legal moves.
    """
    if next_tile == 0:
        # the next move can be anywhere on the board (that is not occupied
        # by a player, or on a big tile that is won)
        return {
            Move(index, player)
            for index in range(81)
            if (bitboard & (1 << index) == 0) and
               (big_bitboard & (1 << (index // 27 * 3 + index % 9 // 3)) == 0)
        }

    if next_tile not in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
        raise ValueError("Invalid next_tile.")

    # the next move can only be in the next_tile, and where there is no player
    return {
        Move(index, player)
        for index in range(81)
        if (bitboard & (1 << index) == 0) and (
                    next_tile & (1 << (index // 27 * 3 + index % 9 // 3)) != 0)
    }


if __name__ == '__main__':
    nums = [num for num in range(81)]
    mapped_nums = map(lambda x: x // 27 * 3 + x % 9 // 3, nums)

    print(list(mapped_nums))
