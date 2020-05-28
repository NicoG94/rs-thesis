
import os
import subprocess

project_path = os.path.dirname(os.path.realpath(__file__))
sys_call = f'pipreqs "{project_path}"'
#print(sys_call)
subprocess.call(sys_call, shell=True)
