import os
import subprocess
from dotenv import load_dotenv


def train_model():
    load_dotenv()
    scripts_dir_path = os.path.dirname(os.path.abspath(__file__))
    repo_dir_path = os.path.join(scripts_dir_path, os.pardir)
    spark_path = os.path.join(os.getenv("SPARK_HOME"), "bin", "spark-submit")
    subprocess.run(f"{spark_path} model/prepare_model.py", shell=True, check=True, cwd=repo_dir_path)


if __name__ == "__main__":
    train_model()
