import copy

from bots import Bot, Evaluation, GameState
from bots.eval.v0_move_order.move_order import MoveOrdering
from ultimate_tic_tac_toe import Player, Move


class JohnBotV2_1(Bot):
    def __init__(self, evaluation: Evaluation,
                 bot_name: str = "johnbot v2.1 move ordering w/ iterative deepening"):
        self.evaluation = evaluation
        self.player = None
        self.game_state = None
        self.bot_name = bot_name
        self.move_ordering = MoveOrdering()

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
        ordered_moves = self.order_moves(list(valid_moves), self.player)
        gamestate_copy = copy.copy(self.game_state)

        # Minimax algorithm with alpha-beta pruning
        best_move = None
        best_score = float('-inf') if self.player == Player.X else float('inf')

        for move in ordered_moves:
            gamestate_copy.push(move)
            score = self.minimax(gamestate_copy,
                                 depth=3,
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

    def order_moves(self, moves: list[Move],
                    maximizing_player: Player) -> list[Move]:
        game_state_copy = copy.copy(self.game_state)
        return self.move_ordering.sort_moves(game_state_copy, moves, maximizing_player)





    def update(self, game_state: GameState) -> None:
        self.game_state = game_state

    def __name__(self) -> str:
        return self.bot_name


if __name__ == '__main__':
    from bots.playable_bots.random_bot import RandomBot
    from bots.eval.pm_eval.powell_merrill_evaluation import PowellMerrillEval
    from bots.bot_game import BotGame

    bot1 = RandomBot()
    bot2 = JohnBotV2_1(PowellMerrillEval())
    evaluation = PowellMerrillEval()
    bot_game = BotGame(bot1, bot2)
    outcome = bot_game.play()
    positions_evaluated = bot2.all_positions_evaluated
    print(outcome)

    print(positions_evaluated)
    print(sum(positions_evaluated) / len(positions_evaluated))
