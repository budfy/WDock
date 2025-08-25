import subprocess
import sys
import os

# Get the path to the virtual environment's Python interpreter
venv_python = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'python.exe')

# Run the main application
subprocess.run([venv_python, 'main.py'])