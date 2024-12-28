from ultimate_tic_tac_toe import Player, Move
import pytest


class TestMoves:
    """
    Because of Mark's mistaken understanding of how the board works, I will
    ensure that the following cases are true when making a move, in turn
    validating that the board works correctly
    """

    def test_moves(self):
        # starting square
        x = Player.X
        move_1 = Move(0, x)
        move_1_algebraic = Move.from_algebraic('A1', x)
        move_1_bitboard = Move.from_bitboard(1, x)
        # the binary number 0b_000000000_000...000_000000001

        assert move_1 == move_1_algebraic
        assert move_1 == move_1_bitboard

        # second square
        o = Player.O
        move_2 = Move(1, o)
        move_2_algebraic = Move.from_algebraic('B1', o)
        move_2_bitboard = Move.from_bitboard(2, o)
        # the binary number 0b_000000000_000...000_000000010

        assert move_2 == move_2_algebraic
        assert move_2 == move_2_bitboard

        # random square
        move_3 = Move(41, x)
        move_3_algebraic = Move.from_algebraic('F5', x)
        move_3_bitboard = Move.from_bitboard(0b000000000_000000000_000000000_000000000_000100000_000000000_000000000_000000000_000000000, x)
        # whatever number this is idk

        assert move_3 == move_3_algebraic
        assert move_3 == move_3_bitboard


