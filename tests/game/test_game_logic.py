import copy

from ultimate_tic_tac_toe import Player, Move, Outcome, Termination, \
    IllegalMoveError
from ultimate_tic_tac_toe.game import Game
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
        game = Game()
        x_turn = True
        for move in generated_move_order:
            real_move = Move.from_algebraic(move, self.x) if x_turn else \
                Move.from_algebraic(move, self.o)
            game.push(real_move)
            x_turn = not x_turn
        # we expect 0 errors

        assert game.outcome == Outcome(Termination.TIC_TAC_TOE, self.x)
        print(game.get_legal_moves())

    def test_illegal_moves(self):
        generated_move_order = ['F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
                                'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
                                'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
                                'F6', 'G9', 'C9', 'I9', 'H9', 'F9', 'H8', 'D6',
                                'A9', 'C7', 'I3', 'H7', 'D2', 'C5', 'I6', 'G7',
                                'B2', 'E6', 'B1']

        # generated game from random bots with an X win on top row
        game_with_illegal = Game()
        x_turn = True
        for move in generated_move_order:
            real_move = Move.from_algebraic(move, self.x) if x_turn else \
                Move.from_algebraic(move, self.o)
            game_with_illegal.push(real_move)
            x_turn = not x_turn

        number_of_moves = len(generated_move_order)
        assert number_of_moves == len(game_with_illegal.made_moves)
        game_copy = copy.copy(game_with_illegal)

        # only legal moves here are f2, e2, d1, and d3
        with pytest.raises(IllegalMoveError):
            game_with_illegal.push(Move.from_algebraic('A1', self.o))

        # ensures that the number of moves is the same
        assert number_of_moves == len(game_with_illegal.made_moves)
        assert game_copy == game_with_illegal

        with pytest.raises(IllegalMoveError):
            game_with_illegal.push(Move.from_algebraic('B1', self.o))

        assert number_of_moves == len(game_with_illegal.made_moves)
        assert game_copy == game_with_illegal

        with pytest.raises(IllegalMoveError):
            game_with_illegal.push(Move.from_algebraic('E2', self.x))

        assert number_of_moves == len(game_with_illegal.made_moves)
        assert game_copy == game_with_illegal

    def test_popping(self):
        generated_move_order = ['F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
                                'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
                                'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
                                'F6', 'G9', 'C9', 'I9', 'H9', 'F9', 'H8', 'D6',
                                'A9', 'C7', 'I3', 'H7', 'D2', 'C5', 'I6', 'G7',
                                'B2', 'E6', 'C1', 'I2', 'H5', 'D4', 'C3', 'I7',
                                'I1', 'H1', 'D1', 'C6', 'G3', 'A8', 'A6']

        # generated game from random bots with an X win on top row
        game = Game()
        with pytest.raises(ValueError):
            game.pop()

        x_turn = True
        for move in generated_move_order:
            real_move = Move.from_algebraic(move, self.x) if x_turn else \
                Move.from_algebraic(move, self.o)
            game.push(real_move)
            x_turn = not x_turn

        game_copy = copy.copy(game)
        next_move = Move.from_algebraic('B7', self.o)
        game.push(next_move)
        popped_move = game.pop()

        assert next_move == popped_move
        assert game_copy == game  # ensures all data is the same

        game.push(next_move)
        game_before_win = copy.copy(game)
        winning_move = Move.from_algebraic('E2', self.x)
        game.push(winning_move)
        popped_move = game.pop()

        assert winning_move == popped_move
        assert game_before_win == game

    def test_draw(self):
        generated_moves = ['e4', 'd3', 'c9', 'g7', 'b1', 'd1', 'a1', 'a3',
                           'b7', 'e3', 'e7', 'f3', 'g9', 'b9', 'f7', 'i2',
                           'g4', 'a2', 'b6', 'd9', 'c8', 'i5', 'h4', 'h3',
                           'd8', 'b5', 'e5', 'd5', 'c4', 'g2', 'a6', 'a7',
                           'c3', 'i8', 'g6', 'a9', 'b8', 'f6', 'g8', 'c5',
                           'h6', 'f9', 'i9', 'i7', 'g3', 'a8', 'a5', 'a4',
                           'b3', 'f8', 'h5', 'd6', 'd4', 'c2', 'b2', 'f5',
                           'i3', 'h9', 'e8', 'f4', 'i1', 'g1', 'e9', 'h1',
                           'h2', 'c6', 'h8', 'h7']
        draw_game = Game()
        x_turn = True
        for move in generated_moves:
            real_move = Move.from_algebraic(move, self.x) if x_turn else \
                Move.from_algebraic(move, self.o)
            draw_game.push(real_move)
            x_turn = not x_turn

        assert draw_game.outcome == Outcome(Termination.DRAW, None)
