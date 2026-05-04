# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Agent, LLM
from config.llm_config import get_llm_params

from tools.dataset_tools import DatasetTools

def get_validator_agent():
    return Agent(
        name="Dataset Validator",
        role="Validate dataset usability",
        goal="""Thoroughly check the dataset for consistency, missing values, and potential biases. 
        Analyze the data quality and detect outliers to decide if the data is high quality enough for reliable business analysis.
        Output in plain text:
        Decision: YES or NO
        Reason: Detailed explanation covering quality metrics and outlier impact.""",
        backstory="A strict dataset gatekeeper. You look for outliers, skewness, and structural integrity using advanced statistical tools.",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.read_dataset_head, 
            DatasetTools.get_dataset_info, 
            DatasetTools.detect_outliers,
            DatasetTools.get_data_quality_report
        ],
        verbose=True
    )

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License
