import torch as t


def parse_bytearray_string_to_sloth_mlp(bytearray: str) -> t.Tensor:
    """
    Converts the string version of the byte array into a tensor for the neural
    network, to use in the sloth bot. This results in a 4 x 81 tensor, where
    the first layer is Xs, the second layer is Os, the third layer is legal
    moves, and the fourth layer is the current player.
    Specifically to be used in the MLP type of neural network for the sloth bot.

    The tensor itself differs from that of use in

    Args:
        bytearray: the bytearray string to convert. not literally a byte array
                but the string representation of one

    Returns:
        the tensor for the neural network
    """
    if len(bytearray) != 93:
        raise ValueError(
            f'Bytearray string is not of the correct length. Expected 92, got {len(bytearray)}')

    x_tensor = t.zeros((81,), dtype=t.int)
    o_tensor = t.zeros((81,), dtype=t.int)
    current_player_tensor = t.ones((81,), dtype=t.int) if bytearray[90] == '2' else t.zeros(
        (81,), dtype=t.int)

    for i, char in enumerate(bytearray[:81]):
        if char == '1':
            x_tensor[i] = 1
        elif char == '2':
            o_tensor[i] = 1

    constraint = int(bytearray[91])
    if constraint == 9:
        legal_moves_tensor = (x_tensor == 0) & (o_tensor == 0)
        legal_moves_tensor = legal_moves_tensor.to(dtype=t.int)
    else:
        legal_moves_tensor = t.zeros((81,), dtype=t.int)
        indices = [
            3 * (constraint % 3) + ((9 * j) + 27 * (constraint // 3)) + i for i
            in range(3) for j in range(3)]
        indices = t.tensor(indices)
        legal_moves_tensor[indices] = (x_tensor[indices] == 0) & (
                    o_tensor[indices] == 0).to(dtype=t.int)
        legal_moves_tensor = legal_moves_tensor.to(dtype=t.int)

    sloth_tensor = t.stack(
        [x_tensor, o_tensor, legal_moves_tensor, current_player_tensor])

    return sloth_tensor


import torch as t


def parse_bytearray_string_to_sloth_cnn(bytearray: str) -> t.Tensor:
    """
    Converts the string version of the byte array into a tensor for the neural
    network, formatted as a (4, 9, 9) tensor.

    Layers:
    - First layer: X's occupied tiles (1 for X, 0 otherwise)
    - Second layer: O's occupied tiles (1 for O, 0 otherwise)
    - Third layer: Legal move positions (1 for valid moves, 0 otherwise)
    - Fourth layer: Current player's turn (1 if X, 0 if O)

    Args:
        bytearray (str): The game state represented as a string.

    Returns:
        t.Tensor: A (4, 9, 9) tensor.
    """

    if len(bytearray) != 93:
        raise ValueError(
            f"Bytearray string is not of the correct length. Expected 92, got {len(bytearray)}")

    # Initialize empty 9x9 tensors
    x_tensor = t.zeros((9, 9), dtype=t.int)
    o_tensor = t.zeros((9, 9), dtype=t.int)
    legal_moves_tensor = t.zeros((9, 9), dtype=t.int)
    current_player_tensor = t.full((9, 9),
                                   1.0 if bytearray[90] == '2' else 0.0,
                                   dtype=t.int)

    # fills xs and os (like that song by Ellie King)
    for index, char in enumerate(bytearray[:81]):
        row = index // 9
        col = index % 9
        if char == '1':
            x_tensor[row, col] = 1.0
        elif char == '2':
            o_tensor[row, col] = 1.0

    # legal move layer
    constraint = int(bytearray[91])
    if constraint == 9:
        legal_moves_tensor = (x_tensor == 0) & (o_tensor == 0)
        legal_moves_tensor = legal_moves_tensor.to(dtype=t.int)
    else:
        indices = [
            3 * (constraint % 3) + ((9 * j) + 27 * (constraint // 3)) + i for i
            in range(3) for j in range(3)]
        row_col = [(i // 9, i % 9) for i in indices]

        for row, col in row_col:
            legal_moves_tensor[row, col] = 1

        legal_moves_tensor = legal_moves_tensor.to(dtype=t.int)

    return t.stack(
        [x_tensor, o_tensor, legal_moves_tensor, current_player_tensor])


if __name__ == '__main__':
    expected_tensor = t.tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                                 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                                 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0]])

