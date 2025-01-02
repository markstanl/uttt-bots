from bots.playable_bots.minimax_2.powell_merrill_evaluation import PowellMerrillEval
from bots import GameState
from ultimate_tic_tac_toe import Move, Player
from ultimate_tic_tac_toe.game import Game

class TestEvaluation:
    def setup_method(self):
        self.evaluation = PowellMerrillEval()
        self.x = Player.X
        self.o = Player.O

    def test_evaluation(self):
        generated_move_order = ['F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
                                'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
                                'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
                                'F6', 'G9', 'C9', 'I9', 'H9', 'F9', 'H8', 'D6',
                                'A9', 'C7', 'I3', 'H7', 'D2', 'C5', 'I6', 'G7',
                                'B2', 'E6', 'B1', 'E2']

        # generated game from random bots with an X win on top row
        game = Game()
        x_turn = True
        for move in generated_move_order:
            real_move = Move.from_algebraic(move, self.x) if x_turn else \
                Move.from_algebraic(move, self.o)
            game.push(real_move)
            x_turn = not x_turn

        print(game)

        initial_eval = self.evaluation.evaluate(GameState(game))
        # O should be destroying
        assert initial_eval < 0

        useless_x_move = Move.from_algebraic('D5', self.x)
        blocking_o_move = Move.from_algebraic('A2', self.o)
        game.push(useless_x_move)
        game.force_push(blocking_o_move)

        blocking_o_eval = self.evaluation.evaluate(GameState(game))
        assert blocking_o_eval < initial_eval
