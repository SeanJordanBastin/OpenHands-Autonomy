import argparse
import os
import sys

# Add root to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Safe fallback loader
try:
    from jarvis.autonomous_agent import Jarvis
except:
    class Jarvis:
        def __init__(self, *args, **kwargs):
            print("⚠️ Using dummy Jarvis agent")
        def run(self):
            return "🤖 Dummy run result"
        task_queue = type("Queue", (), {"empty": lambda: True})()

try:
    from jarvis.task_loader import load_tasks_from_yaml
except:
    def load_tasks_from_yaml(_): return []

def run_task_file(agent, path: str):
    print(f"📄 Loading tasks from {path}")
    try:
        tasks = load_tasks_from_yaml(path)
        for task in tasks:
            agent.task_queue.put(task)
    except Exception as e:
        print(f"❌ Failed to load tasks: {e}")
        return
    agent.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", type=str, required=True)
    args = parser.parse_args()

    agent = Jarvis()
    run_task_file(agent, args.task_file)

