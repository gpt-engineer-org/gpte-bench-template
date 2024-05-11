import yaml
import os
import sys
from typing import List


def read_yaml_file(filename: str) -> List:
    with open(filename, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


def write_yaml_file(filename: str, data: List) -> None:
    with open(filename, 'w') as file:
        yaml.dump(data, file)


def main(results_file: str, scoreboard_file: str):
    result_data = read_yaml_file(results_file)
    if not os.path.isfile(scoreboard_file):
        scoreboard_data = list()
    else:
        scoreboard_data = read_yaml_file(scoreboard_file)
    scoreboard_data.append(result_data)
    write_yaml_file(scoreboard_file, scoreboard_data)

if __name__ == "__main__":
    assert (len(sys.argv) == 3)
    main(sys.argv[1], sys.argv[2])