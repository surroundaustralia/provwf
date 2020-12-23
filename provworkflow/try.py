import subprocess
label = subprocess.check_output(["git", "describe"]).strip()

