from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import from_json
from pyspark.sql.types import DoubleType, IntegerType, LongType, StructField, StructType

from config import config
from model.prediction import proceed_prediction


# Create a Spark session
spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()

# Read the CSV files as a streaming DataFrame
csvStreamDF = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", config.KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", config.KAFKA_TOPIC)
    .option("startingOffsets", "earliest")
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

parsed_df = csvStreamDF.selectExpr("CAST(value AS STRING)").select(from_json("value", schema).alias("features")).select("features.*")

assembler = VectorAssembler(inputCols=config.relevant_columns, outputCol="features")
assembledDF = assembler.transform(parsed_df)
resultDF = proceed_prediction(assembledDF)

# Perform any streaming operations on csvStreamDF as needed
# For example, you can write the streaming data to the console
query = (
    resultDF
    .writeStream
    .outputMode("append")  # or "complete" or "update"
    .format("console")
    .start()
)

# Wait for the termination of the streaming query
query.awaitTermination()
