import os
import subprocess

# get correct path
project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# get requirements.txt
sys_call = f'pipreqs "{project_path}" --force'
print(sys_call)
subprocess.call(sys_call, shell=True)

# move requirements.txt
print("new requirements.txt created")