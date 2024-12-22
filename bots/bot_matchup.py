import time
from bots.Bot import Bot
from bots.bot_game import BotGame


class BotMatchup():
    def __init__(self, bot1: Bot, bot2: Bot, num_games: int = 250):
        self.bot1 = bot1
        self.bot2 = bot2
        self.num_games = num_games
        self.game_state = None
        self.wins = (0, 0, 0) # bot1 wins, bot2 wins, ties
        self.run_time = 0

    def run_simulations(self):
        start_time = time.time()
        for i in range(self.num_games):
            if i % 2 == 0:
                winner = self.run_game(True)
                if winner == 'X':
                    self.wins = (self.wins[0], self.wins[1]+1, self.wins[2])
                elif winner == 'O':
                    self.wins = (self.wins[0]+1, self.wins[1], self.wins[2])
                else:
                    self.wins = (self.wins[0], self.wins[1], self.wins[2] + 1)
            else:
                winner = self.run_game(False)
                if winner == 'X':
                    self.wins = (self.wins[0]+1, self.wins[1], self.wins[2])
                elif winner == 'O':
                    self.wins = (self.wins[0], self.wins[1]+1, self.wins[2])
                else:
                    self.wins = (self.wins[0], self.wins[1], self.wins[2] + 1)

        self.run_time = time.time() - start_time

    def run_game(self, switched: bool):
        if switched:
            game = BotGame(self.bot2, self.bot1)
        else:
            game = BotGame(self.bot1, self.bot2)
        game.play()
        print(game.get_results())
        return game.get_results()['winner']

    def __str__(self):
        return f"Bot1: {self.bot1.__name__()} | Bot2: {self.bot2.__name__()} | Wins: {self.wins} | Time: {self.run_time}"


if __name__ == '__main__':
    from bots.playable_bots.RandomBot.RandomBot import RandomBot
    from bots.playable_bots.minimax_1.minimax_1 import MinimaxPowellMerrill
    bot1 = RandomBot()
    bot2 = MinimaxPowellMerrill()
    matchup = BotMatchup(bot1, bot2, 10)
    matchup.run_simulations()
    print(matchup)
