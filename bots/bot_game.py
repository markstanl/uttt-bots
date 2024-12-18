from bots.Bot import Bot, GameState
from game.ultimate_tic_tac_toe import UltimateTicTacToe


class BotGame:
    def __init__(self, bot1: Bot, bot2: Bot):
        """
        Initialize the game with two playable_bots.
        :param bot1: plays as X
        :param bot2: plays as Y
        """
        self.game = UltimateTicTacToe(event="Bot Game",
                                      x_player=bot1.__name__(),
                                      o_player=bot2.__name__())
        self.player = 'X'
        self.current_player = 'X'
        self.bot1 = bot1
        self.bot2 = bot2
        self.bot1.set_player('X')
        self.bot2.set_player('O')

    def play(self):
        while not self.game.game_over:
            if self.game.current_player == 'X':
                self.bot1.update(GameState(self.game))
                row, col = self.bot1.pick_move()
            else:
                self.bot2.update(GameState(self.game))
                row, col = self.bot2.pick_move()

            self.game.make_valid_move(row, col)

    def get_results(self) -> dict:
        results_dict = {}
        if not self.game.game_over:
            raise ValueError('Game is not over yet')

        if self.game.check_global_tic_tac_toe():
            results_dict['winner'] = f"{self.game.winner}"
        else:
            results_dict['winner'] = "-"
        results_dict['moves'] = self.game.made_moves
        results_dict['final_board'] = self.game.board
        results_dict['game'] = self.game
        return results_dict


if __name__ == '__main__':
    from bots.playable_bots.RandomBot import RandomBot

    bot1 = RandomBot()
    bot2 = RandomBot()
    game = BotGame(bot1, bot2)
    game.play()
    game.game.print_annotated_board()
    print(game.game.made_moves)
    game.game.write_uttt_to_file('example.txt')
