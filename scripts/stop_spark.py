import os
import sys
import subprocess
from dotenv import load_dotenv


def stop_spark():
    load_dotenv()
    spark_sbin_path = os.path.join(os.getenv("SPARK_HOME"), "sbin")
    subprocess.run(os.path.join(spark_sbin_path, "stop-worker.sh"), shell=True, check=True)
    subprocess.run(os.path.join(spark_sbin_path, "stop-master.sh"), shell=True, check=True)


if __name__ == "__main__":
    stop_spark()
