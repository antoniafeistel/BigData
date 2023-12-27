from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf, count

from config import path_handling, data_handling
from model.model_utils import train_model, save_model

# EXTRACT
spark = SparkSession.builder.master(path_handling.SPARK_MASTER).getOrCreate()
csv_read_df = spark.read.csv(path_handling.RAW_DATA_PATH, header=data_handling.CSV_HEADER, sep=data_handling.CSV_SEP, schema=data_handling.schema)

# TRANSFORM
encoded_df = data_handling.encode_df(csv_read_df)
assembler = VectorAssembler(inputCols=data_handling.features, outputCol=data_handling.FEATURES_COL)
assembled_df = assembler.transform(encoded_df)
train_df = assembled_df.select(data_handling.FEATURES_COL, data_handling.LABEL_COL)

# compute sample weights according to binary inverse class frequency for balancing training dataset
alias_count_col = "label_count"
agg_df = train_df.groupby(data_handling.LABEL_COL).agg(count(data_handling.LABEL_COL).alias(alias_count_col))
num_labels_0 = agg_df.where(data_handling.LABEL_COL + " == 0").select(alias_count_col).first()[alias_count_col]
num_labels_1 = agg_df.where(data_handling.LABEL_COL + " == 1").select(alias_count_col).first()[alias_count_col]
num_labels = num_labels_0 + num_labels_1
num_classes = 2
weight_0 = num_labels / (num_classes * num_labels_0)
weight_1 = num_labels / (num_classes * num_labels_1)

assign_weight_udf = udf(lambda is_fraud: weight_0 if is_fraud == 0 else weight_1, DoubleType())
train_df = train_df.withColumn(data_handling.WEIGHT_COL, assign_weight_udf(data_handling.LABEL_COL))

# LOAD
train_df.write.mode("overwrite").parquet(path_handling.TRAIN_DATA_PATH)

# use loaded data for model training
rf_clf_model = train_model(spark)
save_model(rf_clf_model)
