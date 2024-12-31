import pytest
from ultimate_tic_tac_toe.game import Game


class TestTicTacToe:
    def setup_method(self):
        self.bot = Game()

    def test_tic_tac_toe(self):
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
        bitboard = 0b_011100010_110100001_001001000_100000111_101001001_000010010_000000110_000001010_000001001
        big_bitboard = 0b000_001_000
        assert self.bot.check_small_tic_tac_toe(bitboard, 3) == True
        assert self.bot.check_small_tic_tac_toe(bitboard, 4) == False
