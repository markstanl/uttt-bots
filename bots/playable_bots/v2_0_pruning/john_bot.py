import copy

from bots import Bot, Evaluation, GameState
from ultimate_tic_tac_toe import Player, Move


class JohnBotV2(Bot):
    def __init__(self,
                 evaluation: Evaluation,
                 bot_name: str = "v2_0_pruning",
                 depth=3):
        self.depth = depth
        self.evaluation = evaluation
        self.player = None
        self.game_state = None
        self.bot_name = bot_name
        self.all_positions_evaluated = []

    def set_player(self, player: Player) -> None:
        self.player = player

    def pick_move(self) -> Move:
        self.positions_evaluated = 0
        if self.game_state.is_game_over():
            raise ValueError('Game is over')

        if self.game_state.get_current_player() != self.player:
            raise ValueError('Not the bot\'s turn')

        valid_moves = self.game_state.get_legal_moves()
        gamestate_copy = copy.copy(self.game_state)

        best_move = None
        best_score = float('-inf') if self.player == Player.X else float('inf')
        for move in valid_moves:
            gamestate_copy.push(move)
            score = self.minimax(gamestate_copy,
                                 depth=self.depth,
                                 alpha=float('-inf'),
                                 beta=float('inf'),
                                 maximizing=(self.player != Player.X))

            if self.player == Player.X and score > best_score:
                best_score = score
                best_move = move
            elif self.player == Player.O and score < best_score:
                best_score = score
                best_move = move
            gamestate_copy.pop()

        self.all_positions_evaluated.append(self.positions_evaluated)
        return best_move

    def minimax(self,
                game_state: GameState,
                depth: int,
                alpha: float,
                beta: float,
                maximizing: bool) -> float:
        if depth == 0 or game_state.is_game_over():
            return self.evaluation.evaluate(game_state)

        self.positions_evaluated += 1

        if maximizing:
            max_eval = float('-inf')
            for move in game_state.get_legal_moves():
                game_state.push(move)
                curr_eval = self.minimax(game_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, curr_eval)

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    game_state.pop()
                    break

                game_state.pop()
            return max_eval

        else:
            min_eval = float('inf')
            for move in game_state.get_legal_moves():
                game_state.push(move)
                curr_eval = self.minimax(game_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, curr_eval)

                beta = min(beta, min_eval)
                if beta <= alpha:
                    game_state.pop()
                    break

                game_state.pop()
            return min_eval

    def update(self, game_state: GameState) -> None:
        self.game_state = game_state

    def __name__(self) -> str:
        return self.bot_name


if __name__ == '__main__':
    from bots.playable_bots.random_bot import RandomBot
    from bots.eval.pm_eval.powell_merrill_evaluation import PowellMerrillEval
    from bots.bot_game import BotGame

    bot1 = RandomBot()
    evaluation = PowellMerrillEval()
    bot2 = JohnBotV2(evaluation)
    bot_game = BotGame(bot1, bot2)
    outcome = bot_game.play()
    print(outcome)

    positions_evaluated = bot2.all_positions_evaluated
    print(positions_evaluated)
    print(sum(positions_evaluated) / len(positions_evaluated))
