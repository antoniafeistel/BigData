from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import DoubleType, IntegerType, LongType, StructField, StructType
from pyspark.ml.feature import VectorAssembler

from config import path_handling, data_handling
from model.model_utils import predict


spark = SparkSession.builder.master(path_handling.SPARK_MASTER).getOrCreate()

# read .csv files as a streaming DataFrame
csv_stream_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", path_handling.KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", path_handling.KAFKA_TOPIC)
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", 300000)
    .load()
)

schema = StructType([
    StructField("gender", IntegerType(), True),
    StructField("state", IntegerType(), True),
    StructField("city_pop", IntegerType(), True),
    StructField("job", IntegerType(), True),
    StructField("profile", IntegerType(), True),
    StructField("trans_date", IntegerType(), True),
    StructField("unix_time", LongType(), True),
    StructField("category", IntegerType(), True),
    StructField("amt", DoubleType(), True),
    StructField("merchant", IntegerType(), True),
])

parsed_df = csv_stream_df.selectExpr("CAST(value AS STRING)").select(from_json("value", schema).alias(data_handling.FEATURES_COL)).select(data_handling.FEATURES_COL + '.*')
assembler = VectorAssembler(inputCols=data_handling.features, outputCol=data_handling.FEATURES_COL)
assembled_df = assembler.transform(parsed_df)
predicted_df = predict(assembled_df)

query = (
    predicted_df
    .writeStream
    .outputMode("append")  # alternatives: "complete", "update"
    .format("console")
    .start()
)

query.awaitTermination()
