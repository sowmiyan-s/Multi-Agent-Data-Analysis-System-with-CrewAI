import os
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List
from crewai import Crew, Task
from utils.logger import app_logger
from config.app_config import settings
from config.llm_config import get_llm_params

# Import local agents
from agents.cleaner import get_cleaner_agent
from agents.validator import get_validator_agent
from agents.insights import get_insights_agent
from agents.viz_expert import get_viz_expert_agent

class AnalysisResult:
    def __init__(self, status: str, data: Optional[pd.DataFrame] = None, reports: Dict[str, Any] = None, error: Optional[str] = None):
        self.status = status
        self.data = data
        self.reports = reports or {}
        self.error = error

def run_analysis_pipeline(csv_path: str, task_callback=None) -> AnalysisResult:
    """
    Main entry point for the agentic analysis pipeline.
    """
    app_logger.info(f"Starting analysis pipeline for: {csv_path}")
    
    # Pre-flight check: Validate API Key
    llm_params = get_llm_params()
    api_key = llm_params.get("api_key", "")
    is_placeholder = any(x in api_key.lower() for x in ["sk-...", "your_", "key_here", "dummy"])
    
    if (not api_key or is_placeholder) and "ollama" not in llm_params.get("model", ""):
        error_msg = f"Valid API Key missing for provider: {os.getenv('LLM_PROVIDER', settings.DEFAULT_PROVIDER)}. Please set it in the sidebar."
        app_logger.error(error_msg)
        return AnalysisResult(status="error", error=error_msg)

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        app_logger.error(f"Failed to read CSV: {e}")
        return AnalysisResult(status="error", error=f"Read Error: {str(e)}")

    # Initialize Agents
    app_logger.debug("Initializing agents...")
    cleaner = get_cleaner_agent()
    validator = get_validator_agent()
    viz_expert = get_viz_expert_agent()
    strategist = get_insights_agent()

    # Define Tasks
    app_logger.debug("Defining tasks...")
    
    clean_task = Task(
        description=f"Analyze the dataset at {csv_path} and identify data quality issues. Suggest specific cleaning steps.",
        expected_output="A detailed data quality report with recommended cleaning actions.",
        agent=cleaner,
        callback=lambda x: task_callback('clean', x) if task_callback else None
    )

    validate_task = Task(
        description="Verify if the dataset is statistically sound and suitable for business intelligence analysis.",
        expected_output="A validation report with a GO/NO-GO decision.",
        agent=validator,
        context=[clean_task],
        callback=lambda x: task_callback('validate', x) if task_callback else None
    )

    viz_task = Task(
        description="Design 5 interactive visualizations that reveal the most important trends in the data. Provide them as a JSON array.",
        expected_output="A JSON array of 5 objects containing 'title', 'x', 'y', 'type', and 'reason'.",
        agent=viz_expert,
        context=[validate_task],
        callback=lambda x: task_callback('relation', x) if task_callback else None
    )

    insight_task = Task(
        description="Synthesize all findings into 5 actionable strategic business insights.",
        expected_output="5 high-level business insights with supporting evidence from the data.",
        agent=strategist,
        context=[clean_task, validate_task, viz_task],
        callback=lambda x: task_callback('insights', x) if task_callback else None
    )

    # Assemble Crew
    crew = Crew(
        agents=[cleaner, validator, viz_expert, strategist],
        tasks=[clean_task, validate_task, viz_task, insight_task],
        verbose=True,
        process="sequential"
    )

    try:
        app_logger.info("Kicking off crew execution...")
        result = crew.kickoff()
        
        return AnalysisResult(
            status="complete",
            data=df,
            reports={
                "final_raw": str(result),
                "tasks": {
                    "clean": clean_task.output.raw if clean_task.output else None,
                    "validate": validate_task.output.raw if validate_task.output else None,
                    "viz": viz_task.output.raw if viz_task.output else None,
                    "insights": insight_task.output.raw if insight_task.output else None
                }
            }
        )
    except Exception as e:
        app_logger.error(f"Crew execution failed: {e}")
        return AnalysisResult(status="error", error=str(e))

if __name__ == "__main__":
    # CLI mode for testing
    import sys
    if len(sys.argv) > 1:
        res = run_analysis_pipeline(sys.argv[1])
        print(f"Status: {res.status}")
        if res.error: print(f"Error: {res.error}")
    else:
        print("Usage: python crew.py <path_to_csv>")

