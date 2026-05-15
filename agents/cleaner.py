from crewai import Agent, LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import DatasetTools

def get_cleaner_agent():
    return Agent(
        name="Data Integrity Specialist",
        role="Senior Data Quality Engineer",
        backstory="""You have a passion for data cleanliness and structural integrity. 
        You believe that garbage in equals garbage out. 
        You are meticulous about identifying missing data, outliers, and inconsistencies.""",
        goal="""Perform a comprehensive audit of the dataset. 
        Identify all quality issues and provide a clear, actionable list of cleaning steps.
        Your report should be structured and professional.""",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.inspect_dataset, 
            DatasetTools.data_quality_audit, 
            DatasetTools.statistical_profiling
        ],
        verbose=True
    )
