import pytest

from ufen.ufen import load_ufen, save_ufen, InvalidUfenError
from ultimate_tic_tac_toe.game import Game
from ultimate_tic_tac_toe import Move, Player


class TestUfen:
    def test_valid_ufen(self):
        starting_position = "9/9/9/9/9/9/9/9/9 X 0"
        actual_game = load_ufen(starting_position)
        expected_game = Game()
        assert actual_game == expected_game

        b1_position = "9/9/9/9/9/9/9/9/1X7 O 2"
        actual_game = load_ufen(b1_position)
        expected_game.push(Move.from_algebraic("b1", Player.X))

        print(bin(actual_game.next_board_index))
        print(bin(expected_game.next_board_index))
        assert actual_game == expected_game

    def test_invalid_ufen(self):
        invalid_player = "9/9/9/9/9/9/9/9/9 Z 0"
        with pytest.raises(InvalidUfenError):
            load_ufen(invalid_player)

        invalid_board_char = "9/9/9/1Z7/9/9/9/9/9 X 8"
        with pytest.raises(InvalidUfenError):
            load_ufen(invalid_board_char)

        invalid_num_rows = "9/9/9/9/9/9/9/9 X 0"
        with pytest.raises(InvalidUfenError):
            load_ufen(invalid_num_rows)

        # expect no error in first, and an error in the second
        strict_invalid = "9/9/9/1XX6/9/9/8O/9/9 X 2"
        load_ufen(strict_invalid, strict=False)
        with pytest.raises(InvalidUfenError):
            load_ufen(strict_invalid, strict=True)

    def test_complex_game_state(self):
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
            real_move = Move.from_algebraic(move, Player.X) if x_turn else \
                Move.from_algebraic(move, Player.O)
            game.push(real_move)
            x_turn = not x_turn

        ufen = 'X1X1XOOXO/O1X1OX1XO/1OOO1OOOO/XXOOOXOOX/O1O3OXX/1X1OX3O/2X1OXXXX/1XXXX1XOO/2XXOX1OX O 5'
        actual_game = load_ufen(ufen)
        assert actual_game.next_board_index == game.next_board_index

        fenified = save_ufen(game)
        assert fenified == ufen