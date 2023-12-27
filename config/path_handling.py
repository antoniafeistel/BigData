import os

from config import data_handling


INPUT_FOLDER_RAW = 'resources/data/raw'
RAW_DATA_PATH = os.path.join(INPUT_FOLDER_RAW, data_handling.VERSION)
INPUT_FOLDER_TRAIN = 'resources/data/train'
TRAIN_DATA_PATH = os.path.join(INPUT_FOLDER_TRAIN, data_handling.VERSION)
INPUT_FOLDER_TEST = 'resources/data/test'

MODELS_FOLDER = 'resources/models'
MODEL_PATH = os.path.join(MODELS_FOLDER, data_handling.VERSION)

SPARK_MASTER = "spark://LFK66VG60V:7077"

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'regression-test'
KAFKA_CHECKPTS_PATH = 'kafka_checkpoints'
