import os
import subprocess
import pyautogui
from datetime import datetime

# Rerun YAML checker
os.system("bash scripts/wrap_and_check_yamls.sh")

# Screenshot
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"screenshots/wrap_check_{timestamp}.png"
os.makedirs("screenshots", exist_ok=True)
pyautogui.screenshot(filename)
print(f"✅ Screenshot saved to {filename}")


