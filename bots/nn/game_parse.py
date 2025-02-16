from ultimate_tic_tac_toe import Move, Player, Outcome
from ultimate_tic_tac_toe.game import Game
import torch

def game_parse(game: Game) -> torch.Tensor:
    """
    Converts the gamestate into a tensor for the neural network to use, based
    on the specifications from the paper:
        AI AGENTS FOR ULTIMATE TIC-TAC-TOE
        PHIL CHEN, JESSE DOAN, EDWARD XU

    The general idea is to make an 9 x 9 x 4 tensor, which is 4 9x9
    representing the board state for different game information. The first
    layer is Xs, the second layer is Os, the third layer is all marked with
    the same value, 1 if it is X's turn, 0 if it is O's turn, and the fourth
    layer is marked with all valid moves.
    Args:
        game: the current game

    Returns:
        torch.Tensor: the tensor representing the game state (9 x 9 x 4)
    """
    x_layer = torch.tensor([[1 if game.x_bitboard & (1 << (i +9*j)) else 0 for i in range(9)] for j in reversed(range(9))])
    o_layer = torch.tensor([[1 if game.o_bitboard & (1 << (i +9*j)) else 0 for i in range(9)] for j in reversed(range(9))])
    turn_layer = torch.tensor([[1 if game.current_player == Player.X else 0 for _ in range(9)] for _ in range(9)])
    current_player = game.current_player

    legal_moves = game.get_legal_moves()
    if current_player == Player.X:
        valid_moves_layer = torch.tensor([[1 if Move(i + j*9, Player.X) in legal_moves else 0 for i in range(9)] for j in reversed(range(9))])
    else:
        valid_moves_layer = torch.tensor([[1 if Move(i + j*9, Player.O) in legal_moves else 0 for i in range(9)] for j in reversed(range(9))])
    return torch.stack([x_layer, o_layer, turn_layer, valid_moves_layer])

if __name__ == '__main__':
    generated_move_order = ['F1', 'H2', 'E4', 'E3', 'F8', 'H6', 'E9', 'D7',
                            'C2', 'G5', 'B4', 'E1', 'F3', 'I8', 'I5', 'G6',
                            'C8', 'I4', 'G2', 'A5', 'B6', 'F7', 'H3', 'E8',
                            'F6']

    # generated game from random bots with an X win on top row
    game = Game()
    x_turn = True
    for move in generated_move_order:
        real_move = Move.from_algebraic(move, Player.X) if x_turn else \
            Move.from_algebraic(move, Player.O)
        game.push(real_move)
        x_turn = not x_turn
    print(game.get_annotated_board())
    x_layer = torch.tensor([[0, 0, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [0, 1, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 1, 0],
                            [0, 0, 1, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0]])
    o_layer = torch.tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0, 1],
                            [0, 0, 0, 1, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 0],
                            [1, 0, 0, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1],
                            [0, 0, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0, 0]])
    turn_layer = torch.tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    valid_moves_layer = torch.tensor(
        [[0, 0, 0, 0, 0, 0, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    tensor = torch.stack([x_layer, o_layer, turn_layer, valid_moves_layer])
    print(torch.equal(tensor, game_parse(game)))
