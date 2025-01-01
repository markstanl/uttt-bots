import copy

from ultimate_tic_tac_toe import Player, Move, Outcome, Termination, \
    IllegalMoveError
from ultimate_tic_tac_toe.game import Game
from ultimate_tic_tac_toe.move_generator import generate_legal_moves
import pytest


class TestSmallTTTAndFullBB:
    def setup_method(self):
        self.game = Game()

    def test_small_ttt(self):
        # some simple checks
        assert self.game.check_small_tic_tac_toe(0b000_000_001_000_000_001_000_000_001, 0)
        assert self.game.check_small_tic_tac_toe(0b000_000_010_000_000_010_000_000_010, 0)
        assert self.game.check_small_tic_tac_toe(0b000_000_100_000_000_100_000_000_100, 0)
        assert self.game.check_small_tic_tac_toe(0b_000_000_001_000_000_010_000_000_100, 0)
        assert self.game.check_small_tic_tac_toe(0b000_000_111_000_000_000_000_000_000, 0)

        # second board check (1st index)
        assert self.game.check_small_tic_tac_toe(0b000_111_000_000_000_000_000_000_000, 1)
        assert self.game.check_small_tic_tac_toe(0b000_100_000_000_010_000_000_001_000, 1)

        # middle board check
        assert self.game.check_small_tic_tac_toe(0b000_100_000_000_010_000_000_001_000_000_000_000_000_000_000_000_000_000, 4)

    def test_full_board(self):
        # first tile
        assert self.game.check_small_bitboard_is_full(0b_000_000_111_000_000_111_000_000_111, 0)

        # second tile
        assert self.game.check_small_bitboard_is_full(0b_000_111_000_000_111_000_000_111_000, 1)

        # middle board
        assert self.game.check_small_bitboard_is_full(0b000_111_000_000_111_000_000_111_000_000_000_000_000_000_000_000_000_000, 4)
