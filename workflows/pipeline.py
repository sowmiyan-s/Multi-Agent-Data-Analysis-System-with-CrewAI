# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Task
from agents.cleaner import cleaner_agent
from agents.validator import validator_agent
from agents.relation import relation_agent
from agents.insights import insights_agent


clean_task = Task(
    agent=cleaner_agent,
    description="Clean the dataset (data/cleaned_csv.csv). Return a simple bulleted list of the steps you took. DO NOT use JSON. DO NOT use code blocks.",
    expected_output="A plain text bulleted list of cleaning steps. Example:\n- Removed duplicates\n- Imputed missing values"
)

validate_task = Task(
    agent=validator_agent,
    description="Validate the dataset (data/cleaned_csv.csv). Return a simple YES/NO decision and a reason. DO NOT use JSON.",
    expected_output="Plain text decision and reason. Example:\nDecision: YES\nReason: The data is clean and ready."
)

relation_task = Task(
    agent=relation_agent,
    description="Identify 5 key relationships for visualization from 'data/cleaned_csv.csv'. You MUST use the strict format: 'X: [col] | Y: [col] | Type: [plot]'. Use ACTUAL column names only.",
    expected_output="Strictly formatted list. Example:\n- X: Age | Y: Salary | Type: Scatter Plot\n- X: City | Y: Sales | Type: Bar Chart"
)

insight_task = Task(
    agent=insights_agent,
    description="Produce 5 key business insights by synthesizing the findings. Return a simple numbered list. DO NOT use JSON.",
    expected_output="Plain text numbered list of 5 insights. Example:\n1. Sales are increasing...\n2. Customer retention is high..."
)

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License
