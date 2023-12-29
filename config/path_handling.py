import os
from dotenv import load_dotenv

from config import data_handling


INPUT_FOLDER_RAW = os.path.join("resources", "data", "train", "raw")
RAW_DATA_PATH = os.path.join(INPUT_FOLDER_RAW, data_handling.VERSION)
INPUT_FOLDER_TRAIN = os.path.join("resources", "data", "train", "transformed")
TRAIN_DATA_PATH = os.path.join(INPUT_FOLDER_TRAIN, data_handling.VERSION)
INPUT_FOLDER_TEST = os.path.join("resources", "data", "test", "**", "**")

MODELS_FOLDER = os.path.join("resources", "models")
MODEL_PATH = os.path.join(MODELS_FOLDER, data_handling.VERSION)

load_dotenv(data_handling.ENV_VARS_PATH)

SPARK_MASTER = os.getenv("SPARK_MASTER_URL")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_CHECKPTS_PATH = os.path.join("kafka_checkpoints")
