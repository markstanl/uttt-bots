from game.ultimate_tic_tac_toe import UltimateTicTacToe
from bots.Bot import Bot, GameState
from bots.playable_bots.RandomBot import RandomBot


class MultiplayerTerminalPlay:
    def __init__(self):
        self.game = UltimateTicTacToe()
        self.game.print_annotated_board()

    def play(self):
        print("Welcome to Ultimate Tic Tac Toe!")
        print("Listen to the prompts! Or press Ctrl+C to quit.")
        while not self.game.game_over:
            self.game.print_annotated_board()
            print(f"{self.game.current_player}'s turn")
            move = input("Enter your move (e.g. A1): ")
            try:
                row, col = self.game.parse_move(move)
                self.game.make_valid_move(row, col)
            except ValueError as e:
                print(e)
                continue

        if self.game.check_global_tic_tac_toe():
            print(f"{self.game.winner} wins!")
        else:
            print("It's a draw!")


class SingleplayerTerminalPlay:
    def __init__(self, bot: Bot):
        self.game = UltimateTicTacToe()
        self.game.print_annotated_board()
        self.player = 'X'
        self.bot = bot
        while True:
            print('Would you like to play X or O?')
            player = input().upper()
            if player in ['X', 'O']:
                self.player = player
                self.bot.set_player('X' if player == 'O' else 'O')
                break
            print('Invalid player choice. Please enter X or O.')

    def play(self):
        print("Welcome to Ultimate Tic Tac Toe!")
        print("Listen to the prompts! Or enter q.")
        while not self.game.game_over:
            if self.game.current_player == self.player:
                self.game.print_annotated_board()
                move = input("Enter your move (e.g. A1): ")
                if move == 'q':
                    break
                try:
                    row, col = self.game.parse_move(move)
                    self.game.make_valid_move(row, col)
                except ValueError as e:
                    print(e)
                    continue
            else:
                print('Bot is thinking...')
                self.bot.update(GameState(self.game))
                row, col = self.bot.pick_move()
                print(f'Bot chose {self.game.number_to_letter_map[col]}{row + 1}')
                self.game.make_valid_move(row, col)


if __name__ == '__main__':
    game = SingleplayerTerminalPlay(RandomBot())
    game.play()
