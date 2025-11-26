# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Agent, LLM
from config.llm_config import get_llm_params

code_gen_agent = Agent(
    name="Code Generator",
    role="Write visualization code",
    goal="Generate matplotlib/seaborn code to visualize the dataset EXACTLY as is. RULES: 1. Do NOT drop rows. 2. Do NOT remove outliers. 3. Implement the SPECIFIC plot type requested by the analyst: 'bar' -> sns.barplot, 'box' -> sns.boxplot, 'histogram' -> sns.histplot, 'heatmap' -> sns.heatmap, 'scatter' -> sns.scatterplot, 'line' -> sns.lineplot. 4. Use 'plt.show()' for each plot.",
    backstory="You are a Data Visualization Expert who trusts the data. You believe that 'cleaning' often destroys valuable information. You NEVER delete rows or filter data. You are a master of Seaborn and Matplotlib, capable of generating any chart type (Bar, Box, Hist, Heatmap) with perfect syntax.",
    allow_delegation=False,
    llm=LLM(**get_llm_params()),
    verbose=True
)

# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License
