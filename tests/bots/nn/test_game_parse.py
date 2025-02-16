from ultimate_tic_tac_toe import Move, Player, Outcome
from ultimate_tic_tac_toe.game import Game
import torch
from bots.nn.game_parse import game_parse

class TestGameParse():
    def test_parse(self):
        generated_move_order = ['F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
                                'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
                                'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
                                'F6']

        # generated game from random bots with an X win on top row
        game = Game()
        x_turn = True
        for move in generated_move_order:
            real_move = Move.from_algebraic(move, Player.X) if x_turn else \
                Move.from_algebraic(move, Player.O)
            game.push(real_move)
            x_turn = not x_turn
        x_layer = torch.tensor([[0, 0, 0, 0, 1, 0, 0, 0, 0],
                                [0, 0, 1, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 1, 0, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 1],
                                [0, 1, 0, 0, 1, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 1, 0, 1, 0],
                                [0, 0, 1, 0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0, 1, 0, 0, 0]])
        o_layer = torch.tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 1, 0, 0, 0, 1],
                                [0, 0, 0, 1, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 1, 1, 0],
                                [1, 0, 0, 0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 1],
                                [0, 0, 0, 0, 1, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 1, 0, 0, 0, 0]])
        turn_layer = torch.tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        valid_moves_layer = torch.tensor(
            [[0, 0, 0, 0, 0, 0, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        tensor = torch.stack([x_layer, o_layer, turn_layer, valid_moves_layer])
        actual = game_parse(game)
        assert torch.equal(tensor, actual)
