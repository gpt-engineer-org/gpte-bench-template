#!/bin/bash
# The first 4 commands are setup for this shell script
# Get the directory containing the current shell script
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
# Define the name of the scoreboard file, which acts as a long term storage for results
SCOREBOARD_FILE=scoreboard.yaml
# Define the name of the temporary results file exported by gpt-engineer for a single run
RESULTS_FILE=results.yaml
# Make the dir of this template project the cwd
cd $SCRIPT_DIR

# The following lines install and execute the benchmarks
# poetry creates a virtual environment and installs the dependencies indicated in pyproject.toml
poetry install --no-root
# The following command executes the benchmark
#   "poetry run" is equivalent to executing "python", but using the poetry venv
#   "bench" is the executable for the benchmarks that is installed by gpt-engineer
#   "benchmark_agent.py" is a path to a file in which a valid agent implementation resides. What the requirements are is found in "benchmark_agent.py".
#   "bench_config.toml" is a path to a config file with instructions for the benchmark run.
#   "$RESULTS_FILE" gives an (optional) path to a (new) yaml file that the results are written to.
poetry run bench benchmark_agent.py bench_config.toml --yaml-output $RESULTS_FILE
# Make a new entry in $SCOREBOARD_FILE with the results from $RESULTS_FILE
poetry run python add_score_board_entry.py $RESULTS_FILE $SCOREBOARD_FILE

