#!/usr/bin/env python3
import argparse
import os
import sys

# === 🧠 PATH PATCHING FOR JARVIS ==============================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# === 🤖 IMPORT JARVIS AGENT ===================================================
try:
    from jarvis.autonomous_agent import Jarvis
except ModuleNotFoundError as e:
    print(f"❌ Failed to import Jarvis: {e}")
    print("💡 Ensure 'jarvis/autonomous_agent.py' exists and defines `class Jarvis`.")
    sys.exit(1)

# === 📦 TASK LOADER IMPORT OR FALLBACK ========================================
try:
    from jarvis.task_loader import load_tasks_from_yaml
except ModuleNotFoundError:
    print("⚠️ 'jarvis.task_loader' not found — falling back to dummy task loader.")
    def load_tasks_from_yaml(_): return []

# === 🔁 AUTONOMOUS TASK LOOP ==================================================
def run_loop(agent: Jarvis):
    print("🔁 JARVIS entering autonomous loop. Press Ctrl+C to stop.")
    while True:
        result = agent.run()
        print(f"\n🧠 JARVIS completed task:\n{result}\n")
        if agent.task_queue.empty():
            print("✅ All tasks completed. JARVIS is idle.")
            break

# === 📄 RUN TASK FILE =========================================================
def run_task_file(agent: Jarvis, path: str):
    print(f"📄 Loading tasks from: {path}")
    try:
        tasks = load_tasks_from_yaml(path)
        for task in tasks:
            agent.task_queue.put(task)
    except Exception as e:
        print(f"❌ Failed to load tasks: {e}")
        return
    run_loop(agent)

# === 🧠 CLI ENTRYPOINT ========================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch JARVIS agent")
    parser.add_argument("--loop", action="store_true", help="Start the autonomous loop")
    parser.add_argument("--task-file", type=str, help="Path to a YAML task file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    try:
        agent = Jarvis(verbose=args.verbose, debug=args.debug)
    except Exception as e:
        print(f"❌ Failed to initialize Jarvis: {e}")
        sys.exit(1)

    if args.task_file:
        run_task_file(agent, args.task_file)
    elif args.loop:
        run_loop(agent)
    else:
        print("⚠️ No task file or --loop provided. Exiting.")
        sys.exit(1)

