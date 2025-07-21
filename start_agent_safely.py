#!/usr/bin/env python3

import os
import yaml
import json
from openai import OpenAI
from datetime import datetime
import subprocess
from pathlib import Path

# Config
TASKS_DIR = "tasks"
MEMORY_FILE = "fix_memory.json"
BACKUP_DIR = "fixed_backups"

# Init
client = OpenAI()
os.makedirs(BACKUP_DIR, exist_ok=True)

# Memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

# Validation
def is_yaml_valid(content):
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False

# GPT Repair
def ask_gpt_to_fix_yaml(filename, content, error):
    print(f"🧠 Asking GPT to fix: {filename}")
    prompt = f"""You are an AI agent helping repair YAML files.

The file `{filename}` contains invalid YAML syntax:
{error}

Here is the content:
```yaml
{content}
```

Return the FULL corrected YAML only. No explanations."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# Fixing Logic
def fix_all_yaml_tasks():
    memory = load_memory()

    for file in Path(TASKS_DIR).glob("*.yaml"):
        with open(file, "r") as f:
            content = f.read()

        if is_yaml_valid(content):
            print(f"✅ Valid → {file}")
            continue

        print(f"❌ Invalid → {file}")

        error_msg = "invalid YAML"

        if file.name in memory:
            print("🧠 Using memory-based fix...")
            fixed = memory[file.name]
        else:
            fixed = ask_gpt_to_fix_yaml(file.name, content, error_msg)
            memory[file.name] = fixed
            save_memory(memory)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(BACKUP_DIR) / f"{file.stem}_{timestamp}.bak.yaml"

        with open(backup_path, "w") as f:
            f.write(content)
        with open(file, "w") as f:
            f.write(fixed)

        print(f"🛠️ Fixed and saved: {file} (backup in {backup_path})")

# Run
if __name__ == "__main__":
    fix_all_yaml_tasks()

