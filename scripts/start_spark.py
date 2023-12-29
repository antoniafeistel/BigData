import os
import shutil
import subprocess
from dotenv import load_dotenv


def start_spark():
    load_dotenv()

    spark_path = os.getenv("SPARK_HOME")
    spark_conf_path = os.path.join(spark_path, "conf")
    shutil.copy2("spark-env.sh", spark_conf_path)

    spark_sbin_path = os.path.join(spark_path, "sbin")
    subprocess.run(os.path.join(spark_sbin_path, "start-master.sh"), shell=True, check=True)
    subprocess.run(os.path.join(spark_sbin_path, f"start-worker.sh {os.getenv("SPARK_MASTER_URL")}"), shell=True, check=True)


if __name__ == "__main__":
    start_spark()
