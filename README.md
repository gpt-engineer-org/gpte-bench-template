# GPT-Engineer Benchmark Suite Template

This repository serves as a template for creating an agent that interacts with the GPT-Engineer benchmark suite. Follow the instructions below to set up your project.

## Agent Implementation

Edit the benchmarking_agent.py file to implement your custom agent. This file contains a minimal example agent that you should replace with your own logic. Feel free to add any necessary functionality specific to your use case.

## Running the Benchmark

Execute the following command to install your project and run the agent against the benchmark suite:
```
./run.sh
```
run.sh also serves as a reference for how the template project is installed and run.
By default, the results and the configuration will be stored in the file _results.yaml_.
Remember that any api keys required by the implemented agents must be defined. The agent in the template requires OPENAI_API_KEY

## Scoreboard entries

At the end of running the benchmarks with _run.sh_, you will be asked whether you want to make a scoreboard entry. This means that the results from _results.yaml_ will be appended to the file _scoreboard.yaml_. If you choose this, you have the possibility to commit the scoreboard (scoreboard.yaml ONLY) and make a pull request with it to the main repo. If you choose to do this, you will be requested to submit additional information used for reproducing the benchmark, which will be done before the scoreboard entry is merged. The best way to ensure reproducibility is to fork this repo and implement your agent in the benchmark_agent.py file. The benchmark_agent can of course have any number of dependencies from your personal agent repo. If done this way, it is enough to provide a url to the github or gitlab size where the fork is located. If some other setup is used, it is up to you to provide an easy and reliable way for us to reproduce the results. At the end of running _run.sh_, there will be a dialogue where you will be provided with a free text option for how to reproduce your results. Note that, any custom LLM configuration should also be provided. The maintainers of this repo will reject any scoreboard entry PR that is deemed too cumbersome to reproduce.


