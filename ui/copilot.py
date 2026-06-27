# Multi Agent Data Analysis with Crew AI
# Copyright (c) 2025 Sowmiyan S
# Licensed under the MIT License

"""
Interactive AI Data Copilot module.
Accepts a natural language query from the user, generates Python code via LLM,
executes it securely in an isolated subprocess, and returns text results and
new dynamically generated visualizations.
"""

import os
import re
import sys
import textwrap
from pathlib import Path
from crewai import LLM
from config.llm_config import get_llm_params
from tools.dataset_tools import _run_in_subprocess, _strip_markdown_fences


def run_copilot_query(query: str, csv_path: str, output_dir_str: str) -> dict:
    """
    Accepts a user query, generates python code to answer it using the current LLM,
    runs the code in a sandbox, and returns the result (text + potential plot).
    """
    # 1. Initialize LLM using the current session parameters
    llm_params = get_llm_params()
    llm = LLM(**llm_params)

    # 2. Define the output file name for any new plot
    output_dir = Path(output_dir_str)
    output_dir.mkdir(parents=True, exist_ok=True)
    copilot_plot_name = f"copilot_plot_{uuid_short()}.png"
    copilot_plot_path = output_dir / copilot_plot_name

    # Clean up previous copilot plots in this session to keep output clean
    for prev_plot in output_dir.glob("copilot_plot_*.png"):
        try:
            prev_plot.unlink(missing_ok=True)
        except OSError:
            pass

    # 3. Create system instructions for code generation
    prompt = f"""
    You are an expert AI Data Analyst Assistant. You have access to a cleaned CSV dataset at '{csv_path}'.
    The user's query is: "{query}"

    Task:
    Write a complete, self-contained Python script to answer the query.
    1. Read the dataset from '{csv_path}' using pandas.
    2. Perform any required analysis, aggregation, or calculations.
    3. Print the final answer/findings clearly to standard output.
    4. If the user asks for a chart, graph, or plot, generate a professional matplotlib or seaborn visualization and save it exactly to: '{copilot_plot_path.as_posix()}'. Always call 'matplotlib.use("Agg")' before importing pyplot. Call 'plt.close()' after saving.

    Formatting:
    Return ONLY valid Python code enclosed in a ```python ... ``` code block. Do NOT include any explanations or conversational text outside the block.
    """

    try:
        # Generate code using the LLM
        response = llm.call([{"role": "user", "content": prompt}])
        raw_output = response if isinstance(response, str) else str(response)
        
        # Extract and clean code
        code = _strip_markdown_fences(raw_output)

        if not code.strip():
            return {
                "success": False,
                "text": "Failed to generate execution code from the model.",
                "plot_path": None
            }

        # 4. Run the generated code in a sandbox subprocess
        success, exec_output = _run_in_subprocess(code)

        # Check if a plot was successfully generated
        plot_saved = copilot_plot_path.exists() and copilot_plot_path.stat().st_size > 0
        final_plot_path = str(copilot_plot_path) if plot_saved else None

        if success:
            return {
                "success": True,
                "text": exec_output if exec_output.strip() != "(no output)" else "Query executed successfully.",
                "plot_path": final_plot_path
            }
        else:
            return {
                "success": False,
                "text": f"Error running query: {exec_output}",
                "plot_path": None
            }

    except Exception as exc:
        return {
            "success": False,
            "text": f"Copilot execution failed: {exc}",
            "plot_path": None
        }


def uuid_short() -> str:
    import uuid
    return uuid.uuid4().hex[:6]
