"""
The following code refactors the data from the UTTTAI dataset, and stores it
into a hugging face dataset.
"""
import json
import os

from utttai_conversion.utttai_convert import numerical_string_refactor
from utttai_conversion import utttai_to_u3t_dict_int_string


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def jsonlify_line(line: str):
    state_action = line.split('} evaluatedActions{')
    state_split_line = state_action[0].split(' ')
    dict_format = {
        'state': '0',
        'num_visits': 0,
        'num_wins': 0,
        'num_draws': 0,
        'num_losses': 0,
        'actions': []
    }
    jsonl_line = dict_format.copy()
    jsonl_line['state'] = numerical_string_refactor(
        (state_split_line.pop(0).strip())[15:], return_type='str')
    jsonl_line['num_visits'] = int(state_split_line.pop(0))
    jsonl_line['num_wins'] = int(state_split_line.pop(0))
    jsonl_line['num_draws'] = int(state_split_line.pop(0))
    jsonl_line['num_losses'] = int(state_split_line.pop(0))

    for action_line in state_action[1].split(','):
        nums = action_line.split(' ')
        jsonl_line['actions'].append({
            'symbol': int(nums[0]),
            'index': utttai_to_u3t_dict_int_string[nums[1]],
            'num_wins': int(nums[2]),
            'num_draws': int(nums[3]),
            'num_losses': int(nums[4])
        })

    return jsonl_line

def refactor_file(old_file_name: str, new_file_name: str):
    file = read_file(old_file_name)
    jsonl_entries = [jsonlify_line(line) for line in file]

    with open(new_file_name, 'w') as outfile:
        for entry in jsonl_entries:
            json.dump(entry, outfile)
            outfile.write('\n')

def refactor_directory(old_dir: str, new_dir: str):
    files = os.listdir(old_dir)
    for file_name in files:
        old_file_path = os.path.join(old_dir, file_name)
        new_file_path = os.path.join(new_dir, file_name.split('.')[0] + '.jsonl')
        refactor_file(old_file_path, new_file_path)



if __name__ == '__main__':
    current_path = os.getcwd()
    print(current_path)
    old_path = os.path.join(current_path, 'data/stage1-mcts')
    new_path = os.path.join(current_path, 'data/stage1-mcts-refactored')
    refactor_directory(old_path, new_path)
