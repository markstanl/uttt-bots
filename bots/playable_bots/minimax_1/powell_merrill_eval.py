from bots import GameState, Evaluation
from ultimate_tic_tac_toe import Player

class PowellMerrillEval(Evaluation):
    def evaluation(self, game_state: GameState) -> float:
        """
        Evaluates the current game state for the player.
        The evaluation function is based on the Powell-Merrill heuristic.
        """
        if game_state.is_game_over():
            if game_state.get_outcome().winner == Player.X:
                return float('inf')
            elif game_state.get_outcome().winner is None:
                return 0
            else:
                return float('-inf')

        x_big_bitboard = game_state.get_x_big_bitboard()
        o_big_bitboard = game_state.get_o_big_bitboard()
        big_bitboard = x_big_bitboard | o_big_bitboard
        x_bitboard = game_state.get_x_bitboard()
        o_bitboard = game_state.get_o_bitboard()
        bitboard = x_bitboard | o_bitboard

        current_score = 0

        current_score += 100 * bin(game_state.get_x_big_bitboard()).count('1')
        current_score -= 100 * bin(game_state.get_o_big_bitboard()).count('1')

        current_score += 150 * self.check_block(big_bitboard, x_bitboard, o_bitboard, Player.X)
        current_score -= 150 * self.check_block(big_bitboard, x_bitboard, o_bitboard, Player.O)

        for i in range(9):
            pass

        return current_score

    def check_block(self, bitboard: int, x_bitboard: int, o_bitboard: int, player: Player) -> int:
        """
        Check's if the player has blocked the opponent from winning.
        Args:
            bitboard: The 3x3 small or big board to check
            player: The player to check for

        Returns:
            int: The number of blocks
        """
        return 0

    def generate_small_board(self, bitboard: int,
                             small_board_index: int) -> int:
        """
        Generate a 3x3 small board from the 81-bit board and index of small board
        Args:
            bitboard: The 81-bit number representing a player's board.
            small_board_index: Index (0-8) of the small 3x3 board to generate.

        Returns:
            int: The 3x3 small board.
        """
        # Compute row and column offsets for the small board
        row_offset = (small_board_index // 3) * 3
        col_offset = (small_board_index % 3) * 3

        # creates a new 3x3 small board
        small_board = 0
        for row in range(3):
            for col in range(3):
                bit_index = (row_offset + row) * 9 + (col_offset + col)
                small_board |= ((bitboard >> bit_index) & 1) << (row * 3 + col)
        return small_board