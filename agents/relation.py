# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Agent, LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import DatasetTools

def get_relation_agent():
    return Agent(
        name="Relationship Mapper",
        role="Identify data relationships",
        backstory="A pattern-recognition specialist who sees connections where others see chaos. You specialize in identifying which variables drive others and how to best visualize those links.",
        goal="""Analyze the dataset and identify 5 meaningful relationships between columns. 
        For each relationship, specify the X and Y axes and the most appropriate plot type.
        Use the strict format: 'X: [col] | Y: [col] | Type: [plot_type]'.
        Plot types should be one of: Scatter Plot, Bar Chart, Line Chart, or Box Plot.
        Ensure you use EXACT column names as found in the dataset head or info.""",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.read_dataset_head, 
            DatasetTools.get_dataset_info, 
            DatasetTools.get_correlation_matrix,
            DatasetTools.get_statistical_summary
        ],
        verbose=True
    )

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License
