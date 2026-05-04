import logging
import sys
import os
from pathlib import Path
import pandas as pd
import webbrowser
from dotenv import load_dotenv

# Import CrewAI components
try:
    from crewai import Crew, Task, Agent
except ImportError as e:
    print(f"ERROR: {e}\nRun: pip install crewai")
    sys.exit(1)

# Import local components
from agents.cleaner import get_cleaner_agent
from agents.validator import get_validator_agent
from agents.relation import get_relation_agent
from agents.insights import get_insights_agent

load_dotenv()

# Disable CrewAI Telemetry to prevent timeouts
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("opentelemetry").setLevel(logging.ERROR)

def perform_initial_cleaning(csv_path: str) -> tuple[pd.DataFrame, Path]:
    """Performs initial data cleaning and returns the cleaned dataframe and its path."""
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise FileNotFoundError(f"Error reading CSV: {e}")

    # Basic cleaning
    df = df.drop_duplicates()
    
    # Fill numeric missing values with mean
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    # Fill categorical missing values with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
            else:
                df[col] = df[col].fillna("Unknown")

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    cleaned_file_path = data_dir / "cleaned_csv.csv"
    df.to_csv(cleaned_file_path, index=False)
    
    return df, cleaned_file_path

def run_crew(csv_path: str, task_callback=None):
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Cleanup existing visualizations
    for existing_file in output_dir.glob("*.png"):
        existing_file.unlink()
    
    try:
        df, cleaned_file_path = perform_initial_cleaning(csv_path)
    except Exception as e:
        print(f"Initial cleaning failed: {e}")
        return None

    # Update dataset path for agents
    os.environ["CURRENT_DATASET_PATH"] = str(cleaned_file_path.absolute())

    # Initialize Agents
    cleaner = get_cleaner_agent()
    validator = get_validator_agent()
    relation = get_relation_agent()
    insights = get_insights_agent()

    # Define Tasks with callbacks
    def _create_callback(name):
        if task_callback:
            return lambda output: task_callback(name, output)
        return None

    clean_task = Task(
        agent=cleaner,
        description="Clean the dataset (data/cleaned_csv.csv). Return a simple bulleted list of the steps you took. DO NOT use JSON. DO NOT use code blocks.",
        expected_output="A plain text bulleted list of cleaning steps.",
        callback=_create_callback('clean')
    )

    validate_task = Task(
        agent=validator,
        description="Validate the dataset (data/cleaned_csv.csv). Return a simple YES/NO decision and a reason. DO NOT use JSON.",
        expected_output="Plain text decision and reason.",
        callback=_create_callback('validate')
    )

    relation_task = Task(
        agent=relation,
        description="Identify 5 key relationships for visualization from 'data/cleaned_csv.csv'. You MUST use the strict format: 'X: [col] | Y: [col] | Type: [plot]'. Use ACTUAL column names only.",
        expected_output="Strictly formatted list.",
        callback=_create_callback('relation')
    )

    insight_task = Task(
        agent=insights,
        description="Produce 5 key business insights by synthesizing the findings. Return a simple numbered list. DO NOT use JSON.",
        expected_output="Plain text numbered list of 5 insights.",
        callback=_create_callback('insights')
    )

    crew = Crew(
        agents=[cleaner, validator, relation, insights],
        tasks=[clean_task, validate_task, relation_task, insight_task],
        verbose=True,
        max_rpm=20, # Increased for better performance while still protecting against bans
        planning=False
    )

    try:
        result = crew.kickoff()
    except Exception as e:
        print(f"Error during crew execution: {e}")
        return {
            'dataframe': df,
            'status': 'error',
            'error': str(e)
        }
    
    return {
        'dataframe': df,
        'status': 'complete',
        'final_result': str(result.raw if hasattr(result, 'raw') else result)
    }

if __name__ == "__main__":
    default_path = (Path.cwd() / "data" / "TB_Burden_Country.csv").resolve()
    a = input(f"Enter the path to your CSV file (default: {default_path.name}): ") or str(default_path)
    report = run_crew(a)
    if report:
        print("\nAnalysis Complete.")
        print("Multi Agent Data Analysis with Crew AI")
        print("Optimized by Antigravity")

