from typing import Set
from ultimate_tic_tac_toe import Player, Move

SECTIONS = [i // 27 * 3 + i % 9 // 3 for i in range(81)]


def generate_legal_moves(bitboard: int,
                                   big_bitboard: int,
                                   next_tile: int,
                                   player: Player) -> Set[Move]:
    if next_tile == 0:
        return {
            Move(index, player)
            for index in range(81)
            if not (bitboard & (1 << index)) and not (big_bitboard & (1 << SECTIONS[index]))
        }

    if next_tile not in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
        raise ValueError("Invalid next_tile.")

    valid_indices = [i for i in range(81) if next_tile & (1 << SECTIONS[i])]
    return {
        Move(index, player)
        for index in valid_indices
        if not (bitboard & (1 << index))
    }
