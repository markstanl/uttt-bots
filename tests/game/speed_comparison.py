from ultimate_tic_tac_toe.bot_ultimate_tic_tac_toe import BotUltimateTicTacToe
from ultimate_tic_tac_toe import Player, Move
from game.ultimate_tic_tac_toe import UltimateTicTacToe
import time


class UpdatedSpeed:
    def setup_method(self):
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

    def test_legacy_speed(self):
        start_time = time.time()
        for _ in range(self.num_games):
            game = UltimateTicTacToe()
            for move in self.generated_move_order:
                parsed_move = game.parse_move(move)
                game.make_valid_move(parsed_move[0], parsed_move[1])
        legacy_duration = time.time() - start_time
        print(f"Legacy method duration: {legacy_duration:.4f} seconds")
        return legacy_duration

    def test_updated_speed(self):
        start_time = time.time()
        for _ in range(self.num_games):
            game = BotUltimateTicTacToe()
            x_turn = True
            for move in self.generated_move_order:
                parsed_move = Move.from_algebraic(move, Player.X if x_turn else Player.O)
                game.push(parsed_move)
                x_turn = not x_turn
        updated_duration = time.time() - start_time
        print(f"Updated method duration: {updated_duration:.4f} seconds")
        return updated_duration

    def compare_speeds(self):
        print("Starting speed comparison...")
        legacy_duration = self.test_legacy_speed()
        updated_duration = self.test_updated_speed()

        print("\nComparison Results:")
        print(f"Legacy method duration: {legacy_duration:.4f} seconds")
        print(f"Updated method duration: {updated_duration:.4f} seconds")
        print(f"Legacy is slower by {legacy_duration - updated_duration:.4f} seconds")
        print(f"Updated method is {legacy_duration / updated_duration:.2f} times faster")

# Usage
if __name__ == "__main__":
    test_speed = UpdatedSpeed()
    test_speed.setup_method()
    test_speed.compare_speeds()
