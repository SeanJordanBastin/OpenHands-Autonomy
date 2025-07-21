import yaml
import textwrap

def wrap_yaml(content):
    try:
        # Load and immediately dump to ensure it's valid YAML and cleanly formatted
        data = yaml.safe_load(content)
        clean_yaml = yaml.dump(data, sort_keys=False)
        # Wrap the YAML in markdown block
        wrapped = textwrap.dedent(f"""\
        ```yaml
        {clean_yaml.strip()}
        ```""")
        return wrapped
    except Exception as e:
        print(f"❌ Failed to wrap YAML content: {e}")
        return content  # Return original if error occurs

def wrap_task_file(path):
    try:
        with open(path, "r") as f:
            content = f.read()

        wrapped_yaml = wrap_yaml(content)

        wrapped_path = path.replace(".yaml", "_wrapped.yaml")
        with open(wrapped_path, "w") as f:
            f.write(wrapped_yaml)

        print(f"🛠️ Wrapped and saved to {wrapped_path}")
        return wrapped_path
    except Exception as e:
        print(f"❌ Failed to wrap YAML file {path}: {e}")
        return path

