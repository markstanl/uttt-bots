"""
For pruning to be most effective, we generally want to get the best scoring
moves first. This means that we should attempt to sort the moves in order of
what we expect to be best. Also, the goal is to be efficient. For example, just
sorting the static evaluation of the first move is not very helpful, it adds
a few seconds to the bots processing time.

Thus, we will consider efficient ways to sort the moves.
"""
from bots import GameState
from ultimate_tic_tac_toe import Move, Player, SMALL_BITBOARD_CENTER_MASK_ANY


class MoveOrdering:
    def __init__(self):
        self.center_mask = SMALL_BITBOARD_CENTER_MASK_ANY

    def sort_moves(self,
                   game_state: GameState,
                   moves: list[Move],
                   maximizing_player: Player) -> list[Move]:
        """
        Sorts the moves in order of what we expect to be best.
        """
        if maximizing_player == Player.X:
            return sorted(moves,
                          key=lambda move: self.evaluate_x_move(game_state,
                                                                move),
                          reverse=True)
        else:
            return sorted(moves,
                          key=lambda move: self.evaluate_o_move(game_state,
                                                                move),
                          reverse=True)

    def evaluate_x_move(self,
                        game_state: GameState,
                        move: Move) -> int:
        """
        Returns the score of the moves based on the x big bitboard.
        Different function to employ the sort function.

        These numbers are roughly based on the _______XXXXXXX
        """
        current_score = 0
        initial_x_big_bitboard = game_state.get_x_big_bitboard()
        initial_big_bitboard = game_state.get_big_bitboard()

        current_big_tile_index = move.index // 27 * 3 + move.index % 9 // 3
        next_big_tile_index = move.index % 3 + 3 * (move.index // 9 % 3)

        # give a good score for a move that wins a big board
        game_state.push(move)
        if game_state.get_x_big_bitboard() > initial_x_big_bitboard:
            # give varying positive scores for moves in ideal big tiles
            if current_big_tile_index == 4:
                current_score += 100
            if current_big_tile_index in [1, 3, 5, 7]:
                current_score += 50
            else:
                current_score += 30

        # give a negative score for a move that gives O a free move
        # (varies from the hueristic as we really don't want to give O a free move)
        # it will likely not be the best move for X, and we pray will be pruned
        if initial_big_bitboard & (1 << next_big_tile_index):
            current_score -= 150

        # give varying negative scores for moves that put O into ideal tiles
        # only need to consider this if the move doesn't give O a free move
        # kind of making up these numbers
        else:
            if next_big_tile_index in [1, 3, 5, 7]:
                current_score -= 8
            else:
                current_score -= 20

        # give a small little bonus for moves that put X in the center
        if self.center_mask & (1 << move.index):
            current_score += 5

        game_state.pop()
        return current_score

    def evaluate_o_move(self,
                        game_state: GameState,
                        move: Move) -> int:
        """
        It may look like bad practice to write these two functions, but it
        allows us to only perform one if statement in the sort_moves function.
        """
        current_score = 0
        initial_o_big_bitboard = game_state.get_o_big_bitboard()
        initial_big_bitboard = game_state.get_big_bitboard()

        current_big_tile_index = move.index // 27 * 3 + move.index % 9 // 3
        next_big_tile_index = move.index % 3 + 3 * (move.index // 9 % 3)

        # give a good score for a move that wins a big board
        game_state.push(move)
        if game_state.get_o_big_bitboard() > initial_o_big_bitboard:
            # give varying positive scores for moves in ideal big tiles
            if current_big_tile_index == 4:
                current_score += 100
            if current_big_tile_index in [1, 3, 5, 7]:
                current_score += 50
            else:
                current_score += 30

        # give a negative score for a move that gives X a free move
        if initial_big_bitboard & (1 << next_big_tile_index):
            current_score -= 150

        # give varying negative scores for moves that put X into ideal tiles
        else:
            if next_big_tile_index in [1, 3, 5, 7]:
                current_score -= 8
            else:
                current_score -= 20

        # give a small little bonus for moves that put X in the center
        if self.center_mask & (1 << move.index):
            current_score += 5

        game_state.pop()
        return current_score


if __name__ == '__main__':
    # visual test looks good to me :)
    from ultimate_tic_tac_toe.game import Game
    new_generated_move_order = ['F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
                                'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
                                'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
                                'F6', 'H7']
    x_turn = True
    game = Game()
    for move in new_generated_move_order:
        real_move = Move.from_algebraic(move, Player.X) if x_turn else \
            Move.from_algebraic(move, Player.O)
        game.push(real_move)
        x_turn = not x_turn
    game_list = list(game.get_legal_moves())
    game_state = GameState(game)
    orderer = MoveOrdering()
    print(orderer.sort_moves(game_state, game_list, Player.X))
    print(game)
