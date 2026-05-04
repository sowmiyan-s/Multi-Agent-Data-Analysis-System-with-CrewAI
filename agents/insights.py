# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Agent, LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import DatasetTools

def get_insights_agent():
    return Agent(
        name="Business Strategist",
        role="Provide business insights",
        backstory="An expert consultant who transforms raw data into actionable business strategy. You look beyond the numbers to find the 'so what' and 'now what' of any dataset.",
        goal="""Synthesize all findings into 5 powerful, actionable business insights. 
        Each insight should be grounded in the data patterns found by the other agents.
        Focus on trends, anomalies, and opportunities for improvement.
        Return a numbered list of insights. Be professional and strategic.""",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.read_dataset_head, 
            DatasetTools.get_dataset_info, 
            DatasetTools.get_statistical_summary,
            DatasetTools.get_correlation_matrix
        ],
        verbose=True
    )

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License
