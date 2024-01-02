import os
from dotenv import load_dotenv


config_dir_path = os.path.dirname(os.path.abspath(__file__))
repo_dir_path = os.path.join(config_dir_path, os.pardir)

ENV_VARS_PATH = os.path.join(repo_dir_path, "scripts", ".env")
load_dotenv(ENV_VARS_PATH)

INPUT_FOLDER_RAW = os.path.join(repo_dir_path, "resources", "data", "train", "raw")
RAW_DATA_PATH = os.path.join(INPUT_FOLDER_RAW, os.getenv("DATA_VERSION"))
INPUT_FOLDER_TRAIN = os.path.join(repo_dir_path, "resources", "data", "train", "transformed")
TRAIN_DATA_PATH = os.path.join(INPUT_FOLDER_TRAIN, os.getenv("DATA_VERSION"))
INPUT_FOLDER_TEST = os.path.join(repo_dir_path, "resources", "data", "test", "**", "**")

MODELS_FOLDER = os.path.join(repo_dir_path, "resources", "models")
MODEL_PATH = os.path.join(MODELS_FOLDER, os.getenv("DATA_VERSION"))

SPARK_MASTER = os.getenv("SPARK_MASTER_URL")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_CHECKPTS_PATH = os.path.join(repo_dir_path, "kafka_checkpoints")
