import subprocess
import sys


infrastructure_scripts = ["start_spark.py", "train_model.py", "start_kafka.py"]


def start_infrastructure():
    python_exec = sys.executable
    print(python_exec)
    for script in infrastructure_scripts:
        subprocess.run([python_exec, script], check=True)


if __name__ == "__main__":
    start_infrastructure()
