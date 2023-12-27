from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler

from config import path_handling, data_handling
from model.model_utils import train_model, save_model


spark = SparkSession.builder.master(path_handling.SPARK_MASTER).getOrCreate()
csv_read_df = spark.read.csv(path_handling.INPUT_FOLDER_RAW, header=data_handling.CSV_HEADER, sep=data_handling.CSV_SEP, schema=data_handling.schema)

encoded_df = data_handling.encode_df(csv_read_df)
assembler = VectorAssembler(inputCols=data_handling.features, outputCol=data_handling.FEATURES_COL)
assembled_df = assembler.transform(encoded_df)
train_df = assembled_df.select(data_handling.FEATURES_COL, data_handling.LABEL_COL)

rf_clf_model = train_model(train_df)
save_model(rf_clf_model, path_handling.MODEL_PATH)
