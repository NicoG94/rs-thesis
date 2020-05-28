import os
import subprocess
import shutil

# get correct path
file_path = os.path.realpath(__file__)
project_path = os.path.dirname(os.path.dirname(file_path))

# get requirements.txt
sys_call = f'pipreqs "{project_path}" --force'
print(sys_call)
subprocess.call(sys_call, shell=True)

# move requirements.txt
old_path = project_path+r"\\requirements.txt"
new_path = os.path.dirname(os.path.dirname(project_path))+r"\\requirements.txt"
shutil.move(old_path, new_path)
shutil.copyfile(new_path, old_path)

print("new requirements.txt created")