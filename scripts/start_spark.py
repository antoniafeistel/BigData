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
    spark_master_url = os.getenv("SPARK_MASTER_URL")
    subprocess.run(os.path.join(spark_sbin_path, f"start-worker.sh {spark_master_url}"), shell=True, check=True)


if __name__ == "__main__":
    start_spark()
