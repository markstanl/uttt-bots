import re
from game.ultimate_tic_tac_toe import UltimateTicTacToe


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def check_tags(file: str, strict = False) -> bool:
    """
    Validates the presence of required tags in the file header.
    :param file: The file to be validated.
    :param strict: If strict is True, the function will additionally require
    that all tags are either required or optional from standardized UTTT.
    """
    lines = file.splitlines()
    lines = [line.strip() for line in lines]
    required_tags = ["Event", "Site", "Date", "Round", "X", "O", "Result"]
    optional_tags = ["Annotator", "TimeControl", "Time", "Termination"]

    # collects the taglines
    tag_lines = [line for line in lines if line.startswith("[")]
    print()
    print("tag lines")
    print(tag_lines)

    for tag_line in tag_lines:
        tag_line_num = lines.index(tag_line) + 1
        tag_line = tag_line.strip()[1:-1]
        tag = tag_line.split(" ")[0].strip()
        value = " ".join(tag_line.split(" ")[1:]).strip()

        # checks that the split is nonempty
        if tag is None or value is None:
            print(f"Invalid tag on line {tag_line_num}. Check that the tag and value are separated by a space, and that they exist")
            return False

        # checks if the tag value is enclosed in double quotes
        if not value.startswith('"') or not value.endswith('"'):
            print(f"Invalid value for tag {tag} on line {tag_line_num}. Check if the value is enclosed in double quotes.")
            return False

        if tag == "Result":
            if value[1:-1] not in ["1-0", "0-1", "1/2-1/2", "*"]:
                print(f"Invalid value for tag {tag} on line {tag_line_num}. Check if the value is one of 1-0, 0-1, 1/2-1/2, or *.")
                return False

        if tag not in required_tags and tag not in optional_tags:
            if strict:
                print(f"Invalid tag {tag} on line {tag_line_num}. Check if the tag is required or optional.")
                return False
            else:
                print(f"Warning: Non-required and non-optional tag {tag} on line {tag_line_num}")

    # checks if all required tags are present
    tag_values = [(line.split(" ")[0].strip())[1:] for line in tag_lines]
    print()
    print(tag_values)
    print(required_tags)
    for required_tag in required_tags:
        if required_tag not in tag_values:
            print(f"Missing required tag {required_tag}")
            return False

    return True


def check_moves(file, strict=True):
    """
    Validates the moves in the file.
    :param file: the file to be validated
    :param strict: if true, requires all moves to be valid. i.e. the preceding
    move allows the following move.
    :return:
    """
    lines = file.splitlines()
    move_lines = [line for line in lines if not line.startswith("[") and line.strip()]
    move_line = " ".join(move_lines)

    # checks if moves exist
    if not move_line:
        print("No moves found in the file.")
        return False

    all_nums_and_moves = [line.strip() for line in move_line.split(" ") if line.strip() != ""]
    num_regex = re.compile(r'\d+\.')
    move_regex = re.compile(r'[A-I][1-9]')

    move_list = []

    # checks if the moves and numbers are syntactically correct
    move_count = 0  # keeps track of if the next should be a number or move
    for num_or_move in all_nums_and_moves[:-1]:
        if move_count == 0:
            if not num_regex.match(num_or_move):
                print(f"Invalid number {num_or_move}. Ensure that the number is formatted correctly and that there are 2 moves between the number.")
                return False
            move_count += 2

        else:
            if not move_regex.match(num_or_move):
                print(f"Invalid move {num_or_move}. Ensure that the move is formatted correctly.")
                return False
            move_list.append(num_or_move)
            move_count -= 1

    # checks if the last item is a valid ending character
    valid_endings = ["1-0", "0-1", "1/2-1/2", "*"]
    if all_nums_and_moves[-1] not in valid_endings:
        print(f"Invalid ending {all_nums_and_moves[-1]}. Ensure that the ending is one of 1-0, 0-1, 1/2-1/2, or *.")
        return False

    # if strict, ensures the game causes no errors
    if strict:
        game = UltimateTicTacToe()
        for move in move_list:
            try:
                move_tuple = game.parse_move(move)
                game.make_valid_move(move_tuple[0], move_tuple[1])
            except Exception as e:
                print(f"Error in move {move}. Ensure that the moves are valid. Check if the move before allows move {move}.")
                return False

    return True


def check_file(file: str, strict: bool = False) -> bool:
    """
    Validates a file containing a UTTT game.
    :param file: the file to be validated
    :param strict: if true, requires tags and moves to be necessarily valid.
    i.e. the tags must be required or optional, and the moves must allow the
    following move.
    :return: true if the file is valid, false otherwise.
    """
    if not check_tags(file, strict):
        return False
    if not check_moves(file, strict):
        return False
    return True


if __name__ == '__main__':
    file = read_file('example.txt')

    if check_file(file, strict=True):
        print("File is valid.")
    else:
        print("File is invalid.")
