import os
import time
import datetime
import schedule
import subprocess

# Path constants
BASE_DIR = "/Users/seanbastin/Downloads/OpenHands-main"
AGENT_SCRIPT = os.path.join(BASE_DIR, "scripts/agent.py")
LOG_FILE = os.path.join(BASE_DIR, "logs/scheduler.log")

# Task definitions
def run_task(task_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n[{timestamp}] Running task: {task_name}\n"
    with open(LOG_FILE, "a") as log:
        log.write(log_entry)
        try:
            result = subprocess.run(
                ["poetry", "run", "python", AGENT_SCRIPT, "--task-file", f"tasks/{task_name}"],
                cwd=BASE_DIR,
                capture_output=True,
                text=True
            )
            log.write(result.stdout)
            if result.stderr:
                log.write("\n[ERROR]\n" + result.stderr)
        except Exception as e:
            log.write(f"\n[EXCEPTION] {str(e)}\n")

# Schedule tasks
schedule.every().day.at("02:30").do(run_task, task_name="self_test_and_learn.yaml")
schedule.every().day.at("03:00").do(run_task, task_name="self_heal_with_goal_understanding.yaml")
schedule.every().monday.at("04:00").do(run_task, task_name="inject_coding_knowledge.yaml")
schedule.every().day.at("05:00").do(run_task, task_name="data_ingestion.yaml")

# Main loop
print("📆 JARVIS Scheduler started. Monitoring tasks...")
while True:
    schedule.run_pending()
    time.sleep(30)


