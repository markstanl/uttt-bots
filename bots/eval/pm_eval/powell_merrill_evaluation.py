from bots import GameState, Evaluation
from ultimate_tic_tac_toe import Player, Move, WINNING_MASKS, \
    SMALL_BITBOARD_WINNING_MASKS, SMALL_BITBOARD_FULL_TILE_MASK


class PowellMerrillEval(Evaluation):
    def __init__(self):
        self.game_state = None

    def evaluate(self, game_state: GameState) -> float:
        """
        Evaluates the current game state for the player.
        The evaluation function is based on the Powell-Merrill heuristic.
        """
        if not isinstance(game_state, GameState):
            raise Exception("game_state must be of type GameState")

        self.game_state = game_state
        if self.game_state.is_game_over():
            if self.game_state.get_outcome().winner == Player.X:
                return float('inf')
            elif self.game_state.get_outcome().winner is None:
                return 0
            else:
                return float('-inf')

        x_big_bitboard = self.game_state.get_x_big_bitboard()
        o_big_bitboard = self.game_state.get_o_big_bitboard()
        big_bitboard = x_big_bitboard | o_big_bitboard
        x_bitboard = self.game_state.get_x_bitboard()
        o_bitboard = self.game_state.get_o_bitboard()
        bitboard = x_bitboard | o_bitboard

        current_score = 0

        # big board wins are worth 100 points
        current_score += 100 * bin(self.game_state.get_x_big_bitboard()).count('1')
        current_score -= 100 * bin(self.game_state.get_o_big_bitboard()).count('1')

        # big board logic, worth 200 points for two in a row, 150 for blocking
        current_score += self.get_big_score(big_bitboard, x_big_bitboard, o_big_bitboard)

        # small board logic, worth 5 points for two in a row, 20 for blocking
        for i in range(9):
            current_score += self.get_small_score(x_bitboard, o_bitboard, i)

        return current_score

    def order_moves(self, moves: list[Move]) -> list:
        pass

    # TODO: Make this a little quicker
    def get_small_score(self, x_bitboard: int, o_bitboard: int,
                                 index: int) -> int:
        """
        Check's if the player has two in a row on a small board
        Args:
            x_bitboard: the x bitboard
            o_bitboard: the o bitboard
            index: the index of the small board

        Returns:
            int: the updated evaluation score
        """
        winning_masks = SMALL_BITBOARD_WINNING_MASKS
        small_tile_mask = SMALL_BITBOARD_FULL_TILE_MASK
        left_transform_number = index % 3 * 3 + (index // 3 * 27)
        x_small_tile_bitboard = x_bitboard & (small_tile_mask << left_transform_number)
        o_small_tile_bitboard = o_bitboard & (small_tile_mask << left_transform_number)

        current_score = 0
        for mask in winning_masks:
            transformed_mask = mask << left_transform_number
            x_masked = x_small_tile_bitboard & transformed_mask
            o_masked = o_small_tile_bitboard & transformed_mask

            # +5 for X two in a row
            if bin(x_masked).count('1') == 2 and bin(o_masked).count('1') == 0:
                current_score += 5

            # -5 for O two in a row
            if bin(o_masked).count('1') == 2 and bin(x_masked).count('1') == 0:
                current_score -= 5

            # +20 for X blocking O
            if bin(o_masked).count('1') == 2 and bin(x_masked).count('1') == 1:
                current_score += 20

            # -20 for O blocking X
            if bin(x_masked).count('1') == 2 and bin(o_masked).count('1') == 1:
                current_score -= 20

        return current_score

    def get_big_score(self,
                      big_bitboard: int,
                      x_big_bitboard: int,
                      o_big_bitboard: int,
                      two_mult: int = 200,
                      block_mult: int = 150) -> int:
        """
        Combines the logic for checking both blocks on the big board, and two
        in a row to get the score evaluation.
        Args:
            big_bitboard: The big bitboard
            x_big_bitboard: Xs big bitboard
            o_big_bitboard: Os big bitboard
            two_mult: The multiplier for two in a row
            block_mult: The multiplier for blocking

        Returns:
            The score evaluation for the big boards, to be added to the score
            evaluation.
        """
        winning_masks = WINNING_MASKS
        current_score = 0
        for mask in winning_masks:
            # masks the big bitboard to a winning line, and checks if a player
            # has two in a row or is blocked in that line

            if bin(x_big_bitboard & mask).count('1') == 2:
                if bin(o_big_bitboard & mask).count('1') == 0:
                    # X has two in a row unblocked
                    current_score += 1 * two_mult
                else:
                    # X is blocked by O
                    current_score -= 1 * block_mult

            if bin(o_big_bitboard & mask).count('1') == 2:
                if bin(x_big_bitboard & mask).count('1') == 0:
                    # O has two in a row unblocked
                    current_score -= 1 * two_mult
                else:
                    # O is blocked by X
                    current_score += 1 * block_mult

        return current_score



    # TODO: Combine these two functions into one
    def check_big_two_in_a_row(self, bitboard: int,
                               x_bitboard: int,
                               o_bitboard: int,
                               player: Player) -> int:
        """
        Check's if the player has two in a row.
        Args:
            bitboard: The 3x3 small or big board to check
            player: The player to check for

        Returns:
            int: The number of two in a rows
        """
        winning_masks = WINNING_MASKS
        two_in_a_row_count = 0
        if player == Player.X:
            # check how many winning masks X has two in a row
            for mask in winning_masks:
                if bin(x_bitboard & mask).count('1') == 2 and bin(
                        o_bitboard & mask).count('1') == 0:
                    two_in_a_row_count += 1
        else:
            # check how many winning masks O has two in a row
            for mask in winning_masks:
                if bin(o_bitboard & mask).count('1') == 2 and bin(
                        x_bitboard & mask).count('1') == 0:
                    two_in_a_row_count += 1
        return two_in_a_row_count

    def check_big_block(self,
                        bitboard: int,
                        x_bitboard: int,
                        o_bitboard: int,
                        player: Player) -> int:
        """
        Check's if the player has blocked the opponent from winning.
        Args:
            bitboard: The 3x3 small or big board to check
            player: The player to check for

        Returns:
            int: The number of blocks
        """
        winning_masks = WINNING_MASKS
        block_count = 0
        if player == Player.X:
            # check how many winning masks X blocks
            for mask in winning_masks:
                if bin(o_bitboard & mask).count('1') == 2 and bin(
                        x_bitboard & mask).count('1') == 1:
                    block_count += 1
        else:
            # check how many winning masks O blocks
            for mask in winning_masks:
                if bin(x_bitboard & mask).count('1') == 2 and bin(
                        o_bitboard & mask).count('1') == 1:
                    block_count += 1
        return block_count
