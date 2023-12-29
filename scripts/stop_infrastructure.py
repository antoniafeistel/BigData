import subprocess
import sys


infrastructure_scripts = ["stop_spark.py", "stop_kafka.py"]


def stop_infrastructure():
    python_exec = sys.executable
    for script in infrastructure_scripts:
        subprocess.run([python_exec, script], check=True)


if __name__ == "__main__":
    stop_infrastructure()
