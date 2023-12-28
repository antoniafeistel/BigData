import os
from dotenv import load_dotenv


def stop_spark():
    load_dotenv()
    spark_sbin_path = os.path.join(os.getenv("SPARK_HOME"), "sbin")
    os.system(os.path.join(spark_sbin_path, "stop-worker.sh"))
    os.system(os.path.join(spark_sbin_path, "stop-master.sh"))


if __name__ == "__main__":
    stop_spark()
