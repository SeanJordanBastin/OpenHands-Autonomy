import argparse
import yaml
import os
import subprocess

def run_task_file(task_file_path):
    with open(task_file_path, "r") as f:
        task_data = yaml.safe_load(f)

    steps = task_data.get("steps", [])
    for step in steps:
        command = step.get("run")
        if command:
            print(f"\n▶️ Running: {command}\n")
            os.system(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", required=True, help="Path to the YAML task file")
    args = parser.parse_args()

    run_task_file(args.task_file)

