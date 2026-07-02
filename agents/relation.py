# Crewlyze
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

from crewai import Agent, LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import DatasetTools


def make_relation_agent() -> Agent:
    """Factory — creates a fresh Relation Analyst agent with the current LLM config."""
    return Agent(
        name="Analyst",
        role="Identify high-value business correlations and dataset relationships",
        goal=(
            "Identify 5 key column relationships with high business relevance (e.g. comparing "
            "metrics like cost vs revenue, demographic factors vs outcome, or country vs rate, "
            "rather than trivial ID columns or metadata). Output ONLY a list in this exact format:\n"
            "- X: [Column1] | Y: [Column2] | Type: [ChartType]\n"
            "DO NOT output any introductions, explanations, or other text."
        ),
        backstory=(
            "You are a Senior Quantitative Analyst. You have a keen eye for finding statistical "
            "relations that translate to real-world business dynamics. You strictly follow "
            "formatting guidelines and never invent columns that don't exist in the provided profile.\n\n"
            "CRITICAL CHART RULE: If either Column1 (X) or Column2 (Y) is categorical (e.g. contains discrete "
            "values like categories, gender, status, chest pain type 'cp', or classes), do NOT recommend a "
            "'Scatter Plot'. Instead, recommend a 'Bar Chart' or 'Box Plot' or 'Grouped Bar Chart'. Scatter Plots "
            "must only be used for continuous numeric vs continuous numeric variables."
        ),
        allow_delegation=False,
        llm=LLM(**get_llm_params()),
        tools=[DatasetTools.read_dataset_head, DatasetTools.get_correlation_matrix],
        max_iter=3,
        verbose=True,
    )
