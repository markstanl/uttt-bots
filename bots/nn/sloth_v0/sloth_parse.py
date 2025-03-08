import torch as t

def parse_bytearray_string_to_sloth(bytearray: str) -> t.Tensor:
    """
    Converts the string version of the byte array into a tensor for the neural
    network, as a rough recreation of the giraffe chess paper. This results
    in a 81 x 4 tensor, where the first layer is Xs, the second layer is Os,
    the third layer is legal moves, and the fourth layer is the current player.

    It is important to note that in the resulting tensors, the msb and lsb are
    switched from the usual convention.

    Args:
        bytearray:

    Returns:

    """
    x_tensor = t.zeros((81, ))
    o_tensor = t.zeros((81, ))
    current_player_tensor = t.ones((81, )) if bytearray[90] == '2' else t.zeros((81, ))

    for i, char in enumerate(reversed(bytearray[:81])):
        x_tensor[i] = 1 if char == '1' else 0
        o_tensor[i] = 1 if char == '2' else 0

    constraint = int(bytearray[91])
    if constraint == 9:
        legal_moves_tensor = t.ones((81, ))
    else:
        legal_moves_tensor = t.zeros((81, ))
        indices = [3*(2 - constraint % 3) + ((9 * j) + 27 * (2 - constraint // 3)) + i for i in range(3) for j in range(3)]
        legal_moves_tensor[indices] = 1

    sloth_tensor = t.stack([x_tensor, o_tensor, legal_moves_tensor, current_player_tensor])
    return sloth_tensor



if __name__ == '__main__':
    initial_state = '000000000000100000200000000000000020000010000020200020100000000001001000000001200' + '000000000120'
    actual_tensor = parse_bytearray_string_to_sloth(initial_state)
    print(actual_tensor)