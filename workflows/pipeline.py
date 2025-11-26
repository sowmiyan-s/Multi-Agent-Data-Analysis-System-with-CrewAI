# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Task
from agents.cleaner import cleaner_agent
from agents.validator import validator_agent
from agents.relation import relation_agent
from agents.code_gen import code_gen_agent
from agents.insights import insights_agent


clean_task = Task(
    agent=cleaner_agent,
    description="Clean the dataset (data/cleaned_csv.csv) and return JSON steps or [] if none.",
    expected_output="JSON array of cleaning steps or []."
)

validate_task = Task(
    agent=validator_agent,
    description="Validate the dataset (data/cleaned_csv.csv) for analysis. Return JSON {'decision':'YES'|'NO','reason':str}.",
    expected_output="JSON: {'decision':'YES' or 'NO', 'reason':'text'}",
    stop_on_error=False,
)

relation_task = Task(
    agent=relation_agent,
    description="Identify visualization relationships between columns in 'data/cleaned_csv.csv'.",
    expected_output="JSON list of relations like [{'x':'col','y':'col','type':'typr of visualization required for this relation'}]"
)

code_task = Task(
    agent=code_gen_agent,
    description="Generate runnable matplotlib/seaborn code for each relation in 'data/cleaned_csv.csv'.",
    expected_output="Runnable Python code blocks or empty string."
)

insight_task = Task(
    agent=insights_agent,
    description="Synthesize the cleaning, validation, and relationship findings into 5 key insights about the dataset 'data/cleaned_csv.csv'.",
    expected_output="JSON list of insights."
)

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License


