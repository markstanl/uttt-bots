from ultimate_tic_tac_toe import Player, Move, Outcome, InvalidMoveError, \
    IllegalMoveError
from ultimate_tic_tac_toe.move_generator import generate_legal_moves
import pytest


class TestMoveGenerator:
    """The following board is being tested:
        |_|O|_||_|_|O||X|X|_|
        |O|_|_||_|_|O||_|O|X|
        |_|_|_||O|_|_||O|_|_|
        ---------------------
        |X|X|X||_|_|_||_|_|X|
        |O|_|_||O|_|_||X|_|O|
        |_|O|_||_|X|_||_|_|_|
        ---------------------
        |_|X|O||_|_|_||_|_|_|
        |_|X|_||X|_|_||_|_|_|
        |X|_|_||O|_|_||_|_|_|
    """

    def setup_method(self):
        self.bitboard = 0b_011100010_110100001_001001000_100000111_101001001_000010010_000000110_000001010_000001001
        self.big_bitboard = 0b000_001_000

    def test_normal_case(self):
        next_move = 0b_010_000_000
        legal_moves = generate_legal_moves(self.bitboard, self.big_bitboard,
                                           next_move, Player.X)
        assert len(legal_moves) > 0
        expected_legal_moves = {Move(58, Player.X),
                                Move(59, Player.X),
                                Move(66, Player.X),
                                Move(67, Player.X),
                                Move(75, Player.X),
                                Move(76, Player.X)}

        for move in legal_moves:
            assert move in expected_legal_moves

    def test_tic_tac_toe_board(self):
        next_move = 0
        legal_moves = generate_legal_moves(self.bitboard, self.big_bitboard,
                                           next_move, Player.X)
        expected_indicies = [1, 2, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 18,
                             21, 22, 23, 24, 25, 26, 30, 32, 33, 34, 35, 40,
                             41, 43, 48, 49, 50, 51, 52, 54, 55, 56, 58, 59,
                             61, 62, 64, 65, 66, 67, 69, 72, 74, 75, 76, 80]
        expected_legal_moves = {Move(index, Player.X) for index in expected_indicies}
        assert set(legal_moves) == expected_legal_moves

