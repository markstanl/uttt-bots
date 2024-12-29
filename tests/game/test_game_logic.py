from ultimate_tic_tac_toe import Player, Move, Outcome, InvalidMoveError, \
    IllegalMoveError
from ultimate_tic_tac_toe.bot_ultimate_tic_tac_toe import BotUltimateTicTacToe
from ultimate_tic_tac_toe.move_generator import generate_legal_moves
import pytest


class TestGameLogic:
    def setup_method(self):
        self.x = Player.X
        self.o = Player.O

    def test_full_game(self):
        generated_move_order = ['F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
                                'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
                                'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
                                'F6', 'G9', 'C9', 'I9', 'H9', 'F9', 'H8', 'D6',
                                'A9', 'C7', 'I3', 'H7', 'D2', 'C5', 'I6', 'G7',
                                'B2', 'E6', 'C1', 'I2', 'H5', 'D4', 'C3', 'I7',
                                'I1', 'H1', 'D1', 'C6', 'G3', 'A8', 'A6', 'B7',
                                'E2']

        # generated game from random bots with an X win on top row
        game = BotUltimateTicTacToe()
        x_turn = True
        for move in generated_move_order:
            print()
            real_move = Move.from_algebraic(move, self.x) if x_turn else\
                Move.from_algebraic(move, self.o)
            print(real_move.__repr__())
            print(game)
            print(generate_legal_moves(game.bitboard, game.big_bitboard, game.next_board_index, self.x if x_turn else self.o))
            game.push(real_move)
            x_turn = not x_turn
        # we expect 0 errors
