import datetime

from ultimate_tic_tac_toe import Move, Player
from ultimate_tic_tac_toe.game import Game


class InvalidUfenError(Exception):
    pass


def load_ufen(file: str,
              strict: bool = False,
              event="Python UTTT",
              site="N/A",
              date=datetime.date.today(),
              round="-",
              x_player="Unnamed",
              o_player="Unnamed",
              annotator=None,
              time=None,
              time_control=None
              ) -> Game:
    """
    Validates the presence of required tags in the file header.
    If strict is True, also validates that the number of Xs and Os is correct.
    :param file: The file to be validated.
    """
    lines = file.splitlines()
    if len(lines) != 1:
        raise InvalidUfenError("The file must contain exactly one line.")

    split_lines = lines[0].strip().split(" ")

    if len(split_lines) != 3:
        raise InvalidUfenError(
            "The file must contain exactly two parts separated by a space. Ensure you only have 1 space")

    board, current_player, next_board_index = split_lines
    if current_player not in ["X", "O"]:
        raise InvalidUfenError("The current player must be either X or O.")

    next_to_move = Player.X if current_player == "X" else Player.O
    next_board_index = int(next_board_index)
    if next_board_index < 0 or next_board_index > 9:
        raise InvalidUfenError("The next board index must be between 0 and 9.")
    game_next_board_index = 1 << (
                next_board_index - 1) if next_board_index != 0 else 0

    rows = board.split("/")

    if len(rows) != 9:
        raise InvalidUfenError("The board must have 9 rows, separated by '/'.")

    if strict:
        validate_strict_move(board, next_to_move)

    game = Game()

    row_num = 9
    for row in rows:
        possible_index = (row_num - 1) * 9
        for char in row:
            if char.isdigit():
                possible_index += int(char)
            elif char == "X":
                move = Move(possible_index, Player.X)
                game.force_push(move)
                possible_index += 1
            elif char == "O":
                move = Move(possible_index, Player.O)
                game.force_push(move)
                possible_index += 1
            else:
                raise InvalidUfenError(
                    f"Invalid character '{char}' in row {row_num}.")
        row_num -= 1

    game.update_current_player()
    game.next_board_index = game_next_board_index
    return game


def validate_strict_move(board: str, next_to_move: Player):
    """
    Validates that the number of Xs and Os is correct.
    Args:
        board: The board to be validated.
        next_to_move: The player who is next to move.

    Returns:
        True if the board is valid
        InvalidUfenError if the board is invalid
    """
    x_count = 0
    o_count = 0
    for char in board:
        if char == "X":
            x_count += 1
        elif char == "O":
            o_count += 1
    if x_count > o_count + 1:
        raise InvalidUfenError(
            "The number of Xs cannot exceed the number of Os by more than 1.")
    if x_count == o_count and next_to_move == Player.O:
        raise InvalidUfenError(
            "The number of Xs cannot equal the number of Os if it is O's turn.")
    if x_count > o_count and next_to_move == Player.X:
        raise InvalidUfenError(
            "The number of Xs cannot exceed the number of Os if it is X's turn.")
    return True


def save_ufen(game: Game) -> str:
    """
    Saves the game in Ufen format.
    :param game: The game to be saved.
    :return: The game in Ufen format.
    """
    board = ""
    for index in reversed(range(81)):
        if 1 << index & game.bitboard == 0:
            if len(board) > 0 and board[-1].isdigit():
                board = board[:-1] + str(int(board[-1]) + 1)
            else:
                board += "1"
        else:
            if 1 << index & game.x_bitboard != 0:
                board += "X"
            else:
                board += "O"
        if index % 9 == 0 and index != 0:
            board += "/"

    # need to flip the rows
    rows = board.split("/")
    rows = [''.join(list(reversed(row))) for row in rows]
    board = '/'.join(rows)

    current_player = "X" if game.current_player == Player.X else "O"
    next_board_index = int(str(bin(game.next_board_index)).count("0")) if game.next_board_index != 0 else 0
    return f"{board} {current_player} {next_board_index}"
