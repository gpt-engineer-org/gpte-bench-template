import yaml
import os
import sys
from typing import List
from git import Repo

def find_repo_root(file_path):
    # Traverse up from the file's directory to find the repository root
    current_dir = os.path.abspath(os.path.dirname(file_path))
    while True:
        if os.path.isdir(os.path.join(current_dir, '.git')):
            return current_dir
        # Move up one directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        # Break if we've reached the root directory
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    return None


def get_commit_hash(file_path):
    repo_root = find_repo_root(file_path)
    # Initialize a Git repository object
    repo = Repo(repo_root)
    return repo.head.commit.hexsha

def check_changes(file_path):
    repo_root = find_repo_root(file_path)

    # Initialize a Git repository object
    repo = Repo(repo_root)

    # Get the file's relative path within the repository
    rel_file_path = os.path.relpath(file_path, repo_root)

    # Check if the file is modified but not staged
    for diff_item in repo.index.diff(None):
        if diff_item.a_path == rel_file_path:
            print(f"{file_path} has unstaged changes.")
            return True

    # Check if the file is modified and staged
    for diff_item in repo.index.diff('HEAD'):
        if diff_item.a_path == rel_file_path:
            print(f"{file_path} has staged changes.")
            return True

    return False


def read_yaml_file(filename: str) -> List:
    with open(filename, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


def write_yaml_file(filename: str, data: List) -> None:
    with open(filename, 'w') as file:
        yaml.dump(data, file)


def main(results_file: str, scoreboard_file: str):
    answer = input(
        "Do you want to make a scoreboard entry? (y/n)"
    )
    while answer.lower() not in ("y", "n"):
        answer = input("Invalid input. Please enter y or n: ")

    if answer.lower() == "y":
        result_data = read_yaml_file(results_file)
        benchmark_file = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "benchmark_agent.py")
        uncommitted_changes = check_changes(benchmark_file)
        while(uncommitted_changes):
            uncommitted_changes = check_changes(benchmark_file)
            input("For reproducibility, the current git commit of benchmark_agent.py is recorded to the scoreboard. Currently there are uncommitted/unstaged changes, preventing the commit to be saved. When you have staged and commited any current changes to benchmark_agent.py, press enter")

        result_data["commit_hash"] = get_commit_hash(benchmark_file)
        answer = input(
            "Please write the url of a public github/gitlab repo where the current version of the benchmark_agent.py file can be found"
        )
        while ("gitlab.com") not in answer.lower() and ("github.com") not in answer.lower():
            answer = input("The given input is not a url to github or gitlab.")
        result_data["url"] = answer
        answer = input(
            "If you are using an privately hosted LLM, such as Llama3, share necessary configuration details such as model version, size and quantization. If you use a public LLM, leave this field blank (enter)."
        )
        result_data["free_text"] = answer
        if not os.path.isfile(scoreboard_file):
            scoreboard_data = list()
        else:
            scoreboard_data = read_yaml_file(scoreboard_file)
            if scoreboard_data is None:
                scoreboard_data = list()
        scoreboard_data.append(result_data)
        write_yaml_file(scoreboard_file, scoreboard_data)

if __name__ == "__main__":
    assert (len(sys.argv) == 3)
    main(sys.argv[1], sys.argv[2])