# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Agent, LLM
from config.llm_config import get_llm_params

relation_agent = Agent(
    name="Analyst",
    role="Analyze dataset and identify key relationships",
    goal="Analyze the dataset thoroughly and detect all meaningful relationships between its columns, then generate a JSON list in the format [{'x':'col','y':'col','type':'plot_type'}] that maps each relationship to the correct visualization. Select plot types strictly based on data characteristics: use scatter for numeric versus numeric relationships, line exclusively for time indexed or sequential numeric data, bar for categorical versus numeric comparisons, histogram for the distribution of a single numeric feature, box for comparing numeric distributions across categories, and heatmap for correlation patterns between numeric columns. Ensure the output uses a diverse range of visualization types without repeating the same kind unnecessarily and return only valid JSON with no extra explanation",
    backstory="You are a Senior Data Analyst who loves visual storytelling. You know that different data requires different charts. You always look for opportunities to use Bar Charts, Box Plots, and Histograms to make the report engaging.",
    allow_delegation=False,
    llm=LLM(**get_llm_params()),
    verbose=True
)

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License
