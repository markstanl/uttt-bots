"""
Class for handling any and all game logic for an Ultimate Tic Tac Toe game.
"""

import datetime


class UltimateTicTacToe:
    """
    Class for handling any and all game logic for an Ultimate Tic Tac Toe game.

    The game is played on a 9x9 grid, where each cell is a 3x3 tic-tac-toe board.
    A tile is won by getting 3 in a row, either horizontally, vertically, or
    diagonally. And the game is won by getting 3 tiles in a row, on the big
    board.


    Game Logic Methods:
    - make_valid_move(row: int, col: int) -> None: Make a move on the board,
        handles all game logic.
    - resign(player: str) -> None: Resign the game.
    - parse_move(move: str) -> (int, int): Parse a move from algebraic notation
    to row, col.
    - get_valid_moves(char_notation=False) -> list: Get the valid moves for the
    current player.
    - print_annotated_board() -> None: Print a prettier version of the board.

    Game Logic Helpers:
    - finish_game(winner: str) -> None: Finish the game and declare a winner.
    - check_valid_move(row: int, col: int) -> bool: Helper method to check if a
    move is valid.
    - save_move(move: (int, int)) -> None: Save the move to the made_moves list.
    - update_small_board(row: int, col: int) -> None: Update the big tiles
    status with a winner or not.
    - check_for_draw() -> bool: Check if the game is a draw.
    - check_global_tic_tac_toe() -> bool: Check if there is a winner in the
    entire game.
    - check_for_tic_tac_toe(board: list) -> str: Check if there is a winner in
    the given board (3x3).

    """

    def __init__(self, event="Python UTTT", site="N/A",
                 date=datetime.date.today(),
                 round="-", x_player="Unnamed", o_player="Unnamed",
                 annotator=None, time=None, time_control=None):
        """
        Initialize the game.
        """
        self.number_to_letter_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E',
                                     5: 'F',
                                     6: 'G', 7: 'H', 8: 'I'}
        self.letter_to_number_map = {v: k for k, v in
                                     self.number_to_letter_map.items()}
        # The board is a 9x9 grid
        self.board = [['_' for _ in range(9)] for _ in range(9)]
        # Small boards are used to keep track of the state of each 3x3 board
        # called small because they are part of the big board
        self.big_tiles = [['_' for _ in range(3)] for _ in range(3)]
        # Keeps track of the board where the next play can be
        self.next_board_coordinates = [-1, -1]
        self.made_moves = []
        self.current_player = 'X'
        self.winner = None
        self.game_over = False

        # Metadata, for writing to UTTT
        self.event = event
        self.site = site
        self.date = date
        self.round = round
        self.x_player = x_player
        self.o_player = o_player
        self.annotator = annotator
        self.time = time
        self.time_control = time_control
        self.result = '*'
        self.termination = None

    def write_uttt_to_file(self, filename):
        with open(filename, 'w') as f:
            # Write metadata headers
            f.write(f'[Event "{self.event}"]\n')
            f.write(f'[Site "{self.site}"]\n')
            f.write(f'[Date "{self.date}"]\n')
            f.write(f'[Round "{self.round}"]\n')
            f.write(f'[X "{self.x_player}"]\n')
            f.write(f'[O "{self.o_player}"]\n')
            f.write(f'[Result "{self.result}"]\n')
            f.write(f'[Termination "{self.termination}"]\n')
            if self.annotator:
                f.write(f'[Annotator "{self.annotator}"]\n')
            if self.time:
                f.write(f'[Time "{self.time}"]\n')
            if self.time_control:
                f.write(f'[TimeControl "{self.time_control}"]\n')
            f.write('\n')

            # Write moves with line wrapping
            line_length = 0
            for i, moves in enumerate(self.made_moves):
                move_str = f'{i + 1}. {" ".join(moves)} '
                if line_length + len(move_str) > 80:
                    f.write('\n')
                    line_length = 0
                f.write(move_str)
                line_length += len(move_str)

            # Write result on a new line
            f.write(f'{self.result}\n')

    def make_valid_move(self, row: int, col: int):
        """
        Make a move on the board. Under assumption that we have two coordinates
        that are definitively valid.
        :param row: the row of the move
        :param col: the column of the move
        :return:
        """
        # Ensures validity of the move, raises error if invalid
        self.check_valid_move(row, col)

        # Update the board
        self.board[row][col] = self.current_player
        self.update_small_board(row, col)
        self.save_move((row, col))

        # Check for a winner in the entire game
        if self.check_global_tic_tac_toe():
            self.finish_game(self.current_player)
            return

        if self.check_for_draw():
            self.finish_game(self.current_player, draw=True)
            return

        # Switch player
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def finish_game(self, winner, resign=False, draw=False):
        """
        Finish the game and declare a winner.
        """
        self.game_over = True
        winner_player = self.x_player if winner == 'X' else self.o_player
        if draw:
            self.winner = '-'
            self.result = '1/2-1/2'
        else:
            self.winner = winner
            if winner == 'X':
                self.result = '1-0'
            elif winner == 'O':
                self.result = '0-1'

        if resign:
            self.termination = f"{winner_player} wins by resignation"
        else:
            self.termination = f"{winner_player} wins by tic-tac-toe"

    def resign(self, player):
        """
        Resign the game.
        :param player: current player, X or O
        """
        if player == 'X':
            self.finish_game('O', resign=True)
        else:
            self.finish_game('X', resign=True)

    def check_valid_move(self, row: int, col: int):
        """
        Ensures that a given move is valid.
        """
        if self.game_over:
            raise ValueError('Game is over')

        if row < 0 or row > 8 or col < 0 or col > 8:
            raise ValueError('Invalid move')

        if (row, col) not in self.get_valid_moves(char_notation=False):
            raise ValueError('Invalid move')

        return True

    def save_move(self, move: (int, int)):
        """
        Save the move to the made_moves list.
        """
        move = self.number_to_letter_map[move[1]] + str(move[0] + 1)
        if self.current_player == 'X':
            self.made_moves.append([move])
        else:
            self.made_moves[-1].append(move)

    def update_small_board(self, row, col):
        """
        Update the big tiles status with a winner or not.
        """
        big_row, big_col = row // 3, col // 3
        small_board = [self.board[i][big_col * 3:(big_col + 1) * 3] for i in
                       range(big_row * 3, (big_row + 1) * 3)]

        if self.check_for_tic_tac_toe(small_board):
            self.big_tiles[big_row][
                big_col] = self.current_player  # Mark as won
        elif all(cell != '_' for row in small_board for cell in row):
            self.big_tiles[big_row][big_col] = '-'  # Mark as tied

        # Update current board coordinates
        next_board_row, next_board_col = row % 3, col % 3
        if self.big_tiles[next_board_row][next_board_col] in (
                'X', 'O', '-'):
            self.next_board_coordinates = [-1, -1]  # Allow global moves
        else:
            self.next_board_coordinates = [next_board_row, next_board_col]

    def get_valid_moves(self, char_notation=False):
        """
        Get the valid moves for the current player.
        :param char_notation: if true, returns in algebraic notation
        (e.g. '1A'), else returns as a list of tuples of the form (row, col)
        """
        if self.game_over:
            raise ValueError('Game is over')

        valid_moves = []
        target_board = self.next_board_coordinates

        if target_board == [-1, -1]:  # Any move is allowed
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == '_' and self.big_tiles[i // 3]\
                            [j // 3] not in ('X', 'O', '-'):
                        valid_moves.append((i, j))

        else:  # Restrict to the target small board
            start_row, start_col = target_board[0] * 3, target_board[1] * 3
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if self.board[i][j] == '_':
                        valid_moves.append((i, j))

        if char_notation:
            return [self.number_to_letter_map[col] + str(row + 1) for row, col
                    in
                    valid_moves]

        return valid_moves

    def check_for_draw(self):
        """
        Checks if the game is a draw.
        :return: True if the game is a draw, False otherwise.
        """
        for small_board in self.big_tiles:
            if any(cell == '_' for cell in small_board):
                return False
        return True

    def check_global_tic_tac_toe(self):
        """
        Check if there is a winner in the entire game.
        """
        return self.check_for_tic_tac_toe(self.big_tiles)

    def check_for_tic_tac_toe(self, board):
        """
        Check if there is a winner in the given board (3x3).
        Returns 'X' if X wins, 'O' if O wins, None if no winner.
        Does so by checking rows, columns, and diagonals.
        """
        for i in range(3):
            # Check rows and columns
            if board[i][0] == board[i][1] == board[i][2] and board[i][
                0] != '_':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] and board[0][
                i] != '_':
                return board[0][i]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '_':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '_':
            return board[0][2]

        return None

    def parse_move(self, move: str) -> (int, int):
        """
        Parse the move from UTTT notation (e.g. '1A') to row, col.
        """
        if len(move) != 2:
            raise ValueError('Invalid move format')
        move = move.upper()
        row = int(move[1]) - 1
        col = self.letter_to_number_map.get(move[0])
        if row < 0 or row > 8 or col is None:
            raise ValueError('Invalid move')
        return row, col

    def print_annotated_board(self):
        """
        Prints a prettier version of the board with annotations.
        """

        x_win = ['X   X', '  X  ', 'X   X']
        o_win = [' OOO ', 'O   O', ' OOO ']

        print('Annotated Board:')
        print('   A B C D E F G H I')

        for big_row in range(3):
            for small_row in range(3):
                # Print dividing lines for big boards
                if small_row == 0 and big_row > 0:
                    print('  ------+-----+------')

                # Print row label for the left-most column
                print(f'{big_row * 3 + small_row + 1} ',
                      end='')

                row_output = []  # Accumulate strings for the row
                for big_col in range(3):
                    # Check if the big board is won and by whom
                    small_board = self.board[big_row * 3 + small_row][
                                  big_col * 3:(big_col + 1) * 3]
                    big_board_winner = self.check_for_tic_tac_toe(
                        [self.board[big_row * 3 + i][
                         big_col * 3:big_col * 3 + 3]
                         for i in range(3)])

                    if big_board_winner == 'X':
                        row_output.append(x_win[small_row])
                    elif big_board_winner == 'O':
                        row_output.append(o_win[small_row])
                    else:
                        row_output.append(' '.join(small_board))

                # Print with | at the start, between, and end of big boards
                print('|' + '|'.join(row_output) + '|')

    def __str__(self):
        """
        More brutalist version of the board.
        """
        return_string = ''
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                return_string += '---------------------\n'
            for j, space in enumerate(row):
                if j % 3 == 0:
                    return_string += '|'
                return_string += space + '|'
            return_string += '\n'
        return return_string

    def __repr__(self):
        return self.__str__() + f'\nCurrent Player: {self.current_player}' + f'\n Next Small Square ${self.next_board_coordinates}' + f'\nWinner: {self.winner}' + f'\nGame Over: {self.game_over}'


if __name__ == '__main__':
    game = UltimateTicTacToe()
