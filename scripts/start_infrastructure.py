import subprocess
import sys


infrastructure_scripts = ["start_spark.py", "start_kafka.py"]


def start_infrastructure():
    python_exec = sys.executable
    for script in infrastructure_scripts:
        subprocess.run([python_exec, script], check=True)


if __name__ == "__main__":
    start_infrastructure()
