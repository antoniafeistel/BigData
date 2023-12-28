import os
import subprocess
from dotenv import load_dotenv


def start_producer():
    load_dotenv()
    parent_directory = os.path.join(os.getcwd(), os.pardir)
    spark_path = os.path.join(os.getenv("SPARK_HOME"), "bin", "spark-submit")
    subprocess.run(f"{spark_path} --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 --conf spark.cores.max=1 producer/producer.py", shell=True, check=True, cwd=parent_directory)


if __name__ == "__main__":
    start_producer()
