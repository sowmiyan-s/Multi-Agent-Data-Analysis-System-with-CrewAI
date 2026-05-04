from crew import run_crew
import os
import json

def test_workflow():
    print("Starting Production Workflow Test...")
    test_file = "data/test_production_data.csv"
    
    if not os.path.exists(test_file):
        print(f"Error: {test_file} not found.")
        return

    # Define a simple callback to track progress
    def progress_callback(step, output):
        print(f"Agent Finished: {step}")

    # Run the crew
    print("AI Agents are analyzing the test data...")
    result = run_crew(test_file, task_callback=progress_callback)

    if result and result.get('status') == 'complete':
        print("\nWorkflow Test SUCCESSFUL!")
        print("-" * 50)
        print(f"Cleaned Dataframe Shape: {result['dataframe'].shape}")
        print("Final analysis successfully completed.")
        print("-" * 50)
    else:
        print(f"\nWorkflow Test FAILED: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_workflow()
