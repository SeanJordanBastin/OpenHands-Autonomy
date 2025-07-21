import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TASKS_DIR = "tasks"
BROKEN_FILES = [
    "self_heal_with_chatgpt.yaml",
    "upgrade_agent_full_auto.yaml",
    "enable_auto_yaml_fixing.yaml",
    "self_writing_loop.yaml"
]

def ask_gpt_to_fix(file_name, content, error_msg):
    prompt = f"""
The following YAML file has a parsing error. Please fix the error and return only valid YAML.

Filename: {file_name}
Error: {error_msg}

Broken YAML:
{content}

Return fixed YAML only (no explanation).
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a YAML repair assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def fix_yaml_file(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read()
        yaml.safe_load(content)
        print(f"✅ Already valid: {file_path}")
    except Exception as e:
        print(f"🛠️ Repairing {file_path} with GPT...")
        fixed = ask_gpt_to_fix(file_path, content, str(e))
        fixed_path = file_path.replace(".yaml", "_fixed.yaml")
        with open(fixed_path, "w") as f:
            f.write(fixed)
        print(f"✅ Saved repaired file: {fixed_path}")

if __name__ == "__main__":
    for file in BROKEN_FILES:
        fix_yaml_file(os.path.join(TASKS_DIR, file))

