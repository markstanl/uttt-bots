import copy

from bots import Bot, Evaluation, GameState
from ultimate_tic_tac_toe import Player, Move


class MCTS(Bot):
    def __init__(self,
                 evaluation: Evaluation,
                 bot_name: str = "MCTS"):
        self.evaluation = evaluation
        self.player = None
        self.game_state = None
        self.bot_name = bot_name

        # really only for debugging purposes
        self.positions_evaluated = 0
        self.all_positions_evaluated = []

    def set_player(self, player: Player) -> None:
        self.player = player

    def pick_move(self) -> Move:
        self.positions_evaluated = 0

        # Basic checks to ensure the bot can make a move
        if self.game_state.is_game_over():
            raise ValueError('Game is over')

        if self.game_state.get_current_player() != self.player:
            raise ValueError('Not the bot\'s turn')

        # Get and order the valid moves
        valid_moves = self.game_state.get_legal_moves()
        gamestate_copy = copy.copy(self.game_state)

        



    def update(self, game_state: GameState) -> None:
        self.game_state = game_state

    def __name__(self) -> str:
        return self.bot_name


if __name__ == '__main__':
    from bots.playable_bots.random_bot import RandomBot
    from bots.eval.pm_eval.powell_merrill_evaluation import PowellMerrillEval
    from bots.bot_game import BotGame

    bot1 = RandomBot()
    bot2 = MCTS(PowellMerrillEval())
    evaluation = PowellMerrillEval()
    bot_game = BotGame(bot1, bot2)
    outcome = bot_game.play()
    positions_evaluated = bot2.all_positions_evaluated
    print(outcome)

    print(positions_evaluated)
    print(sum(positions_evaluated) / len(positions_evaluated))
