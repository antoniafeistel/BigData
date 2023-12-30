import os
import subprocess
import sys


infrastructure_scripts = ["start_spark.py", "start_kafka.py"]


def start_infrastructure():
    scripts_dir_path = os.path.dirname(os.path.abspath(__file__))
    python_exec = sys.executable
    for script in infrastructure_scripts:
        subprocess.run([python_exec, script], check=True, cwd=scripts_dir_path)


if __name__ == "__main__":
    start_infrastructure()
