import subprocess
import shutil
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_dir, "windows.sh")
bash = shutil.which("bash") or "/bin/bash"

subprocess.call(["chmod", "+x", script_path])
subprocess.call([bash, script_path])