from bots.Bot import GameState


def powell_merrill_evaluation(game_state: GameState) -> int:
    winner_evals = {'X': 10000, 'O': -10000, '-': 0}
    if game_state.is_game_over():
        return winner_evals[game_state.get_winner()]

    score = 0
    current_board = game_state.get_board()
    big_tiles = game_state.get_big_tiles()

    # handles big tile evaluation
    for i, big_row in enumerate(big_tiles):
        for j, big_tile in enumerate(big_row):
            if big_tile == '_':
                continue
            modifier = 1 if big_tile == 'X' else -1
            score += modifier * 100
            score += modifier * 100 * check_close_tiles(current_board, i, j,
                                                        big_tile)
            score += modifier * 150 * check_for_blocking(current_board, i, j,
                                                         big_tile)

    # handles small tile evaluation
    for i, row in enumerate(current_board):
        for j, tile in enumerate(row):
            if tile == '_':
                continue
            small_board = [current_board[r][(j // 3) * 3:(j // 3) * 3 + 3] for
                           r in range((i // 3) * 3, (i // 3) * 3 + 3)]
            # calculates the small board (3x3 grid from big tile)
            modifier = 1 if tile == 'X' else -1
            score += modifier * 2 * check_close_tiles(small_board, i % 3,
                                                      j % 3, tile)
            score += modifier * 20 * check_for_blocking(small_board, i % 3,
                                                        j % 3, tile)

    return score


def check_for_blocking(board: list, row: int, col: int, player: str) -> int:
    count = check_row_blocking(board, row, col, player)
    count += check_column_blocking(board, row, col, player)
    if row == col:
        count += check_left_diagonal_blocking(board, row, col, player)
    if row + col == 2:
        count += check_right_diagonal_blocking(board, row, col, player)
    return count


def check_row_blocking(board: list, row: int, col: int, player: str) -> int:
    return 1 if all(board[row][c] != player or c == col for c in range(3)) else 0


def check_column_blocking(board: list, row: int, col: int, player: str) -> int:
    return 1 if all(board[r][col] != player or r == row for r in range(3)) else 0


def check_left_diagonal_blocking(board: list, row: int, col: int,
                                 player: str) -> int:
    return 1 if all(
        board[i][i] != player or (i == row and i == col) for i in range(3)) else 0


def check_right_diagonal_blocking(board: list, row: int, col: int,
                                  player: str) -> int:
    return 1 if all(
        board[i][2 - i] != player or (i == row and 2 - i == col) for i in
        range(3)) else 0


def check_close_tiles(board: list, row: int, col: int, player: str) -> int:
    return (check_row(board, row, col, player) +
            check_column(board, row, col, player) +
            check_left_diagonal(board, row, col, player) +
            check_right_diagonal(board, row, col, player))


def check_row(board: list, row: int, col: int, player: str) -> int:
    return 1 if any(board[row][c] == player and c != col for c in range(3)) else 0


def check_column(board: list, row: int, col: int, player: str) -> int:
    return 1 if any(board[r][col] == player and r != row for r in range(3)) else 0


def check_left_diagonal(board: list, row: int, col: int, player: str) -> int:
    return 1 if any(
        board[i][i] == player and (i != row or i != col) for i in range(3)) else 0


def check_right_diagonal(board: list, row: int, col: int, player: str) -> int:
    return 1 if any(
        board[i][2 - i] == player and (i != row or 2 - i != col) for i in
        range(3)) else 0
