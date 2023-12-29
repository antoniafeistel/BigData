import os
import sys
import subprocess
from dotenv import load_dotenv


def start_producer():
    load_dotenv()
    scripts_dir_path = os.path.dirname(os.path.abspath(__file__))
    repo_dir_path = os.path.join(scripts_dir_path, os.pardir)
    spark_path = os.path.join(os.getenv("SPARK_HOME"), "bin", "spark-submit")
    producer_path = os.path.join("producer", "producer.py")
    subprocess.run(f"{spark_path} --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 --conf spark.cores.max=1 {producer_path}", shell=True, check=True, cwd=repo_dir_path)


if __name__ == "__main__":
    try:
        start_producer()
    except KeyboardInterrupt:
        sys.exit(0)
