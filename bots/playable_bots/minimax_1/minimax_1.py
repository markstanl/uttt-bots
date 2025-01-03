import random
import cProfile
import pstats
from abc import ABC
from typing import Tuple

from bots.__init__ import Bot, GameState
from bots.playable_bots.minimax_1.powell_merrill_eval import powell_merrill_evaluation


class MinimaxPowellMerrill(Bot, ABC):
    def __init__(self):
        self.player = None
        self.game_state = None
        self.evaluated_moves = 0

    def set_player(self, player: str) -> None:
        self.player = player

    def pick_move(self) -> Tuple[int, int]:
        if self.game_state.is_game_over():
            raise ValueError('Game is over')

        if self.game_state.get_current_player() != self.player:
            raise ValueError('Not the bot\'s turn')

        valid_moves = self.game_state.get_legal_moves()
        best_move = None
        best_score = float('-inf') if self.player == 'X' else float('inf')

        # Profiling for pick_move
        profiler = cProfile.Profile()
        profiler.enable()

        for move in valid_moves:
            self.evaluated_moves += 1
            new_gamestate = self.game_state.copy()
            new_gamestate.make_move(move[0], move[1])
            score = self.minimax(new_gamestate, depth=3,
                                 maximizingPlayer=(self.player != 'X'))

            if self.player == 'X' and score > best_score:
                best_score = score
                best_move = move
            elif self.player == 'O' and score < best_score:
                best_score = score
                best_move = move

        profiler.disable()

        # Save profiling stats to a file
        with open('pick_move_profile.txt', 'w') as f:
            stats = pstats.Stats(profiler, stream=f)
            stats.strip_dirs()
            stats.sort_stats('cumulative')
            stats.print_stats()

        print('move made:', best_move)
        print('evaluated moves:', self.evaluated_moves)
        self.evaluated_moves = 0
        return best_move

    def minimax(self, gamestate: GameState, depth: int, maximizingPlayer):

        self.evaluated_moves += 1

        # Do not enable profiling here to avoid conflict
        if depth == 0 or gamestate.is_game_over():
            return powell_merrill_evaluation(gamestate)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in gamestate.get_valid_moves():
                new_gamestate = gamestate.copy()
                new_gamestate.make_move(move[0], move[1])
                eval = self.minimax(new_gamestate, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            for move in gamestate.get_valid_moves():
                new_gamestate = gamestate.copy()
                new_gamestate.make_move(move[0], move[1])
                eval = self.minimax(new_gamestate, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval

    def update(self, game_state: GameState) -> None:
        self.game_state = game_state

    def __name__(self):
        return "Minimax Powell Merrill Eval"


if __name__ == '__main__':
    from bots.playable_bots.random_bot.random_bot import RandomBot
    from bots.bot_game import BotGame

    bot1 = RandomBot()
    bot2 = MinimaxPowellMerrill()
    game = BotGame(bot1, bot2)
    game.play()
    game.game.print_annotated_board()
    print(game.game.made_moves)
    game.game.write_uttt_to_file('example2.txt')