#!/bin/bash

# Get the directory containing the current shell script
script_dir=$(dirname "$(readlink -f "$0")")
cd $script_dir
poetry install --no-root
# poetry shell
PYTHONPATH=.:$PYTHONPATH poetry run bench benchmark_agent.py bench_config.toml

