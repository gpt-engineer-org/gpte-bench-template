#!/bin/bash

# Get the directory containing the current shell script
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Define the name of the scoreboard file, which acts as a long term storage for results
SCOREBOARD_FILE=scoreboard.yaml

# Define the name of the temporary results file exported by gpt-engineer for a single run
RESULTS_FILE=results.yaml

cd $SCRIPT_DIR
poetry install --no-root
# poetry shell
PYTHONPATH=.:$PYTHONPATH poetry run bench benchmark_agent.py bench_config.toml --yaml-output $RESULTS_FILE
PYTHONPATH=.:$PYTHONPATH poetry run python add_score_board_entry.py $RESULTS_FILE $SCOREBOARD_FILE

