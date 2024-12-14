# Moo-tual Agents (Snowvation): AI Multi-agent generation for Marketing Strategy

## Introduction

This project demonstrates the use of the CrewAI framework to automate the creation of a marketing strategy. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.

## Quickstart

- Copy `.env.example` to `.env` and set up the environment variables for [OpenAI](https://platform.openai.com/api-keys) and other tools as needed, like [Serper](serper.dev).
  - Use `python src/marketing_posts/test.py` to check azure openai connection.
- Run `pip3 install -e .` to install the package
- (Optionally) Add custom inputs to `run_inputs.json`. Each input should include a `customer_domain` and `project_description`.
- Run `run_inputs` to run the multi-agent marketing strategy generation for all inputs in `run_inputs.json`.
  - This will run with both intermediate reflection and the E2E evaluator. Each run may take a few minutes to complete.
  - To only run a single entry, set the `domain_filter` environment variable (e.g `domain_filter=snowflake.com run_inputs`)


## CrewAI Framework

CrewAI is designed to facilitate the collaboration of role-playing AI agents. In this example, these agents work together to create a comprehensive marketing strategy and develop compelling marketing content.

## Key Code Pointers

- `src/marketing_posts/`: Contains the baseline code for the marketing strategy generation.
- `src/marketing_posts_e2e_eval/`: Contains the code for marketing strategy generation with an e2e evaluator and a reflection agent introduced with each task.
  - `src/marketing_posts_e2e_eval/main.py`: Main entry point for the marketing strategy generation with the e2e evaluator.
  - `src/marketing_posts_e2e_eval/marketing_crew/config/tasks.yaml`: Contains the task definitions for the marketing strategy generation tasks
  - `src/marketing_posts_e2e_eval/marketing_crew/config/agents.yaml`: Contains the agent definitions for the marketing strategy generation agents
  - `src/marketing_posts_e2e_eval/marketing_crew/marketing_crew.py`: Defines the marketing crew and orchestrates the agents to generate the marketing strategy.

