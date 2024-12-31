from ultimate_tic_tac_toe.game import Game
from ultimate_tic_tac_toe import Player, Move
import cProfile
import pstats
import io


class UpdatedSpeed:
    def __init__(self):
        self.generated_move_order = [
            'F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
            'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
            'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
            'F6', 'G9', 'C9', 'I9', 'H9', 'F9', 'H8', 'D6',
            'A9', 'C7', 'I3', 'H7', 'D2', 'C5', 'I6', 'G7',
            'B2', 'E6', 'C1', 'I2', 'H5', 'D4', 'C3', 'I7',
            'I1', 'H1', 'D1', 'C6', 'G3', 'A8', 'A6', 'B7',
            'E2'
        ]
        self.num_games = 1000

    def test_updated_speed(self):
        """
        Runs the updated speed test using BotUltimateTicTacToe.
        """
        for _ in range(self.num_games):
            game = Game()
            x_turn = True
            for move in self.generated_move_order:
                parsed_move = Move.from_algebraic(move, Player.X if x_turn else Player.O)
                game.push(parsed_move)
                x_turn = not x_turn

    def profile_updated_speed(self):
        """
        Profiles the test_updated_speed method to identify bottlenecks.
        """
        profiler = cProfile.Profile()
        profiler.enable()
        self.test_updated_speed()
        profiler.disable()

        # Output profiling results
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream).sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        print(stream.getvalue())


# Usage
if __name__ == "__main__":
    updated_speed = UpdatedSpeed()
    updated_speed.profile_updated_speed()
