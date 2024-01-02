import os
import sys
import subprocess
from dotenv import load_dotenv


def start_consumer():
    load_dotenv()
    scripts_dir_path = os.path.dirname(os.path.abspath(__file__))
    repo_dir_path = os.path.join(scripts_dir_path, os.pardir)
    spark_path = os.path.join(os.getenv("SPARK_HOME"), "bin", "spark-submit")
    consumer_path = os.path.join("consumer", "consumer.py")
    subprocess.run(f"{spark_path} --packages {os.getenv("KAFKA_PACKAGE")} --conf spark.cores.max={os.getenv("CONSUMER_CORES_MAX")} --conf spark.executor.memory={os.getenv("CONSUMER_EXECUTOR_MEMORY")} {consumer_path}",
                   shell=True, check=True, cwd=repo_dir_path)


if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        sys.exit(0)
