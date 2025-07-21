import sys
import yaml
from pathlib import Path

def infer_type_from_command(command):
    if any(x in command.lower() for x in ["curl", "poetry run", "npm", "node", "python"]):
        return "run"
    if any(x in command.lower() for x in ["create", "write", "generate"]):
        return "generate"
    if any(x in command.lower() for x in ["edit", "modify", "replace"]):
        return "edit"
    if any(x in command.lower() for x in ["ask", "question", "prompt"]):
        return "ask"
    return "run"

def sanitize_yaml(filepath):
    try:
        with open(filepath, "r") as f:
            raw = f.read()
            # Try best effort to load malformed YAML
            data = yaml.safe_load(raw)
    except Exception as e:
        print(f"⚠️  Failed to parse YAML: {e}")
        print("🛠️ Attempting to repair basic formatting...")
        lines = raw.splitlines()
        fixed_lines = []
        for line in lines:
            if ":" not in line and line.strip() and not line.strip().startswith("#"):
                fixed_lines.append(f"{line.strip()}:")
            else:
                fixed_lines.append(line)
        try:
            data = yaml.safe_load("\n".join(fixed_lines))
        except Exception as e:
            print(f"❌ Still failed to parse YAML after fix attempt: {e}")
            return

    if not isinstance(data, dict):
        data = {"task": {"name": "Auto-fixed Task", "steps": []}}

    if "task" not in data:
        data["task"] = {"name": "Auto-added task", "steps": []}

    if "steps" not in data["task"]:
        data["task"]["steps"] = []

    steps = data["task"]["steps"]

    for i, step in enumerate(steps):
        if isinstance(step, str):
            # Convert plain string step to structured step
            inferred = infer_type_from_command(step)
            steps[i] = {inferred: step}
        elif isinstance(step, dict):
            if not any(k in step for k in ("run", "edit", "generate", "ask")):
                if "command" in step:
                    inferred = infer_type_from_command(step["command"])
                    content = step.pop("command")
                    if inferred == "run":
                        step["run"] = content
                    else:
                        step[inferred] = {
                            "path": step.get("file", "unknown.py"),
                            "prompt": content
                        }
                step.pop("file", None)

    out_path = Path(filepath)
    out_fixed = out_path.with_name(out_path.stem + "_fixed.yaml")

    with open(out_fixed, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    print(f"✅ Sanitized YAML saved to: {out_fixed}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/yaml_sanitizer.py tasks/<file>.yaml")
    else:
        sanitize_yaml(sys.argv[1])

