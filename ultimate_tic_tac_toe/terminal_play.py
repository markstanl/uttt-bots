import datetime

from bots import Bot, GameState
from ultimate_tic_tac_toe import Player, Move
from ultimate_tic_tac_toe.game import Game


class MultiPlayerGame:
    def __init__(self,
                 event="Python UTTT",
                 site="N/A",
                 date=datetime.date.today(),
                 round="-",
                 x_player="Terminal Player 1",
                 o_player="Terminal Player 2",
                 annotator=None,
                 time=None,
                 time_control=None):
        self.game = Game(event=event,
                         site=site,
                         date=date,
                         round=round,
                         x_player=x_player,
                         o_player=o_player,
                         annotator=annotator,
                         time=time,
                         time_control=time_control)
        self.x = Player.X
        self.o = Player.O
        self.current_player = self.x

    def play(self):
        print("Welcome to Ultimate Tic Tac Toe!")
        print("Listen to the prompts! Or press Ctrl+C or q to quit.")
        while not self.game.outcome:
            print(self.game.get_annotated_board())
            print(f"{self.game.current_player}'s turn")
            move = input("Enter your move (e.g. A1): ")
            if move == 'q':
                break
            try:
                move = Move.from_algebraic(move, self.current_player)
                self.game.push(move)
                self.current_player = self.o if self.current_player == self.x else self.x
            except ValueError as e:
                print(e)
                continue
        print(self.game.outcome)


class SinglePlayerGame:
    def __init__(self,
                 bot: Bot,
                 event="Python UTTT",
                 site="N/A",
                 date=datetime.date.today(),
                 round="-",
                 annotator=None,
                 time=None,
                 time_control=None,
                 player_name="Terminal Player"):
        self.bot = bot
        self.x = Player.X
        self.o = Player.O

        response = None
        while response not in ['X', 'O']:
            response = input('Would you like to play X or O? ').upper()

        if response == 'X':
            x_player = player_name
            o_player = self.bot.__name__()
            self.bot_player = self.o
            self.bot.set_player(self.o)
        else:
            x_player = "Bot"
            o_player = self.bot.__name__()
            self.bot_player = self.x
            self.bot.set_player(self.x)

        self.game = Game(event=event,
                         site=site,
                         date=date,
                         round=round,
                         x_player=x_player,
                         o_player=o_player,
                         annotator=annotator,
                         time=time,
                         time_control=time_control)

    def play(self):
        print("Welcome to Ultimate Tic Tac Toe!")
        print("Listen to the prompts! Or enter q.")
        while not self.game.outcome:
            print(self.game.get_annotated_board())
            print(f"{self.game.current_player}'s turn")
            if self.game.current_player == self.bot_player:
                print('Bot is thinking...')
                self.bot.update(GameState(self.game))
                move = self.bot.pick_move()
                print(f"Bot chose {move}")
                self.game.push(move)
            else:
                move = input("Enter your move (e.g. A1): ")
                if move == 'q':
                    break
                try:
                    move = Move.from_algebraic(move, self.x)
                    self.game.push(move)
                except ValueError as e:
                    print(e)
                    continue
        print(self.game.outcome)



if __name__ == '__main__':
    from bots.playable_bots.v1_minimax.minimax import Minimax2
    from bots.eval.pm_eval.powell_merrill_evaluation import PowellMerrillEval
    bot = Minimax2(PowellMerrillEval())
    game = SinglePlayerGame(bot)
    game.play()
