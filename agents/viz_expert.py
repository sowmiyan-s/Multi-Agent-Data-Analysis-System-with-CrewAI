from crewai import Agent, LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import DatasetTools

def get_viz_expert_agent():
    return Agent(
        name="Visualization Expert",
        role="Senior Data Visualization Architect",
        backstory="""You are a world-class expert in information design. 
        You don't just make charts; you tell stories with data. 
        You are proficient in Plotly, Seaborn, and D3.js.""",
        goal="""Analyze the dataset and provide exactly 5 high-impact visualizations in a VALID JSON format.
        Each visualization must be an object with: 'title', 'x', 'y', 'type', and 'reason'.
        Types allowed: 'scatter', 'bar', 'line', 'box', 'histogram', 'pie'.
        IMPORTANT: Return ONLY the JSON array. No preamble, no markdown blocks.
        
        Example:
        [{"title": "Revenue Growth", "x": "month", "y": "revenue", "type": "line", "reason": "Trend analysis"}]""",
        llm=LLM(**get_llm_params()),
        tools=[
            DatasetTools.inspect_dataset,
            DatasetTools.statistical_profiling,
            DatasetTools.identify_correlations
        ],
        verbose=True,
        allow_delegation=False
    )
