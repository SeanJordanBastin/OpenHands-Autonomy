import sys
from gpt_tools import fix_yaml_with_gpt  # Replace with your GPT integration method

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "--file":
        print("Usage: --file <filename>")
        sys.exit(1)

    file = sys.argv[2]
    print(f"🤝 Asking GPT to fix {file}...")
    fix_yaml_with_gpt(file)

