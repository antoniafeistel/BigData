import os
import subprocess
import sys


infrastructure_scripts = ["stop_spark.py", "stop_kafka.py"]


def stop_infrastructure():
    scripts_dir_path = os.path.dirname(os.path.abspath(__file__))
    python_exec = sys.executable
    for script in infrastructure_scripts:
        subprocess.run([python_exec, script], check=True, cwd=scripts_dir_path)


if __name__ == "__main__":
    stop_infrastructure()
