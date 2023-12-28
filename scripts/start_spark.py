import os
from dotenv import load_dotenv


def start_spark():
    load_dotenv()

    spark_path = os.getenv("SPARK_HOME")
    spark_conf_path = os.path.join(spark_path, "conf")
    os.system(f"cp -f spark-env.sh {spark_conf_path}")

    spark_sbin_path = os.path.join(spark_path, "sbin")
    os.system(os.path.join(spark_sbin_path, "start-master.sh"))
    os.system(os.path.join(spark_sbin_path, f"start-worker.sh {os.getenv("SPARK_MASTER_URL")}"))


if __name__ == "__main__":
    start_spark()
