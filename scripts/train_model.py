import os
import subprocess
from dotenv import load_dotenv


def train_model():
    load_dotenv()
    parent_directory = os.path.join(os.getcwd(), os.pardir)
    spark_path = os.path.join(os.getenv("SPARK_HOME"), "bin", "spark-submit")
    subprocess.run(f"{spark_path} model/prepare_model.py", shell=True, check=True, cwd=parent_directory)


if __name__ == "__main__":
    train_model()
