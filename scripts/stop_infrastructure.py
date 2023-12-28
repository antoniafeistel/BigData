import subprocess
import sys
import os
import shutil


infrastructure_scripts = ["stop_spark.py", "stop_kafka.py"]


def stop_infrastructure():
    python_exec = sys.executable
    for script in infrastructure_scripts:
        subprocess.run([python_exec, script], check=True)

    kafka_checkpts_path = "../kafka_checkpoints"
    if os.path.exists(kafka_checkpts_path):
        shutil.rmtree(kafka_checkpts_path)


if __name__ == "__main__":
    stop_infrastructure()
