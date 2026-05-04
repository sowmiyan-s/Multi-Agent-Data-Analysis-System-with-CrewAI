# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Agent, LLM
from config.llm_config import get_llm_params

from tools.dataset_tools import DatasetTools

def get_cleaner_agent():
    return Agent(
        name="Data Cleaner",
        role="Report data cleaning steps",
        backstory="A no-nonsense data mechanic who hates messy CSVs. You grew up debugging trash datasets and built a rep for turning corrupt data into clean, analysis-ready gold.",
        goal="""Review the initial automated cleaning performed on the dataset. 
        Analyze the missing values, duplicates, and data types.
        List exactly what was done to clean the data and what further cleaning might be recommended.
        Return a concise bulleted list. DO NOT use JSON.""",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.read_dataset_head, 
            DatasetTools.get_dataset_info, 
            DatasetTools.get_statistical_summary
        ],
        verbose=True
    )

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License
