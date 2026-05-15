from crewai import Agent, LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import DatasetTools

def get_insights_agent():
    return Agent(
        name="Business Strategist",
        role="Principal Business Intelligence Consultant",
        backstory="""You have spent decades advising Fortune 500 CEOs. 
        You can see patterns in data that others miss. 
        You excel at translating technical metrics into strategic business value.""",
        goal="""Synthesize findings from the data audit, validation, and visualizations. 
        Deliver 5 high-impact business insights that can drive revenue or efficiency improvements.""",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.statistical_profiling, 
            DatasetTools.inspect_dataset
        ],
        verbose=True
    )
