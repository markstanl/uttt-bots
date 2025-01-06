from ultimate_tic_tac_toe.game import Game
from ultimate_tic_tac_toe import Move, Player, Outcome
from bots import Bot, GameState


class BotGame:
    def __init__(self, bot1: Bot, bot2: Bot):
        """
        Initializes a BotGame instance with two bots.
        Args:
            bot1: First Bot, playing as X
            bot2: Second Bot, playing as O
        """
        self.bot1 = bot1
        self.bot1.set_player(Player.X)
        self.bot2 = bot2
        self.bot2.set_player(Player.O)
        self.game = Game(event="Bot Game",
                         x_player=bot1.__name__(),
                         o_player=bot2.__name__())

    def play(self) -> Outcome:
        while True:
            if self.game.current_player == Player.X:
                self.bot1.update(GameState(self.game))
                move = self.bot1.pick_move()
            else:
                self.bot2.update(GameState(self.game))
                move = self.bot2.pick_move()

            self.game.push(move)
            if self.game.outcome is not None:
                return self.game.outcome

    def get_outcome(self) -> Outcome:
        return self.game.get_outcome()


if __name__ == '__main__':
    from bots.playable_bots.random_bot import RandomBot
    from bots.playable_bots.minimax_2.minimax_2 import Minimax2
    from bots.playable_bots.minimax_2.powell_merrill_evaluation import PowellMerrillEval
    bot1 = RandomBot()
    evaluation = PowellMerrillEval()
    bot2 = Minimax2(evaluation)
    bot_game = BotGame(bot1, bot2)
    outcome = bot_game.play()
    print(outcome)
