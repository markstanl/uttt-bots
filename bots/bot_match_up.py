from typing import List

from bots import Bot
from bots.bot_game import BotGame
from ultimate_tic_tac_toe import Player


class MatchUpOutcome:
    def __init__(self):
        self.bot1_wins = 0
        self.bot2_wins = 0
        self.draws = 0

    def add_bot1_win(self):
        self.bot1_wins += 1

    def add_bot2_win(self):
        self.bot2_wins += 1

    def add_draw(self):
        self.draws += 1

    def is_empty(self):
        return self.bot1_wins == 0 and self.bot2_wins == 0 and self.draws == 0

    def __str__(self):
        return f"Bot 1 wins: {self.bot1_wins}, Bot 2 wins: {self.bot2_wins}, Draws: {self.draws}"


class BotMatchUp:
    def __init__(self, bot1: Bot, bot2: Bot, print_games: bool = False):
        self.bot1 = bot1
        self.bot2 = bot2
        self.outcome = MatchUpOutcome()
        self.bot_games = []
        self.print_games = print_games

    def play(self, num_games=1000) -> None:
        if not self.outcome.is_empty():
            self.outcome = MatchUpOutcome()

        bot1_is_x = True
        for _ in range(num_games):
            # play game switching between X and O for each bot
            if bot1_is_x:
                bot_game = BotGame(self.bot1, self.bot2)
            else:
                bot_game = BotGame(self.bot2, self.bot1)

            if self.print_games:
                print("Game is starting")

            bot_game.play()
            self.bot_games.append(bot_game)

            if self.print_games:
                print(f"X Player: {bot_game.game.x_player}, O Player: {bot_game.game.o_player} Winner: {bot_game.get_outcome().winner}")

            # update the get_outcome
            if bot_game.get_outcome().winner == Player.X:
                if bot1_is_x:
                    self.outcome.add_bot1_win()
                else:
                    self.outcome.add_bot2_win()
            elif bot_game.get_outcome().winner == Player.O:
                if bot1_is_x:
                    self.outcome.add_bot2_win()
                else:
                    self.outcome.add_bot1_win()
            else:
                self.outcome.add_draw()

            bot1_is_x = not bot1_is_x

    def get_outcome(self) -> MatchUpOutcome:
        return self.outcome

    def get_games(self) -> List[BotGame]:
        return self.bot_games


if __name__ == '__main__':
    from bots.playable_bots.random_bot import RandomBot
    from bots.eval.pm_eval.powell_merrill_evaluation import \
        PowellMerrillEval
    from bots.playable_bots.v1_minimax.minimax import Minimax2
    from bots.playable_bots.v2_1_move_order.john_bot import JohnBotV2_1

    bot1 = JohnBotV2_1(PowellMerrillEval())
    bot2 = RandomBot()
    bot_match_up = BotMatchUp(bot1, bot2, print_games=True)
    bot_match_up.play(10)
    print(bot_match_up.get_outcome())
