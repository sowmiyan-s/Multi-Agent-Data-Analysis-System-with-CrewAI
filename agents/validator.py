from crewai import Agent, LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import DatasetTools

def get_validator_agent():
    return Agent(
        name="Statistical Auditor",
        role="Senior Statistical Analyst",
        backstory="""With a PhD in Statistics, you are the final gatekeeper of data validity. 
        You check for sampling bias, statistical significance, and whether the data distribution 
        makes sense for the intended business analysis.""",
        goal="""Evaluate the statistical validity of the dataset. 
        Provide a rigorous assessment of whether the data can be trusted for high-stakes decision making.""",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.statistical_profiling, 
            DatasetTools.identify_correlations,
            DatasetTools.inspect_dataset
        ],
        verbose=True
    )
