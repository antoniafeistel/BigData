from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType
from pyspark.ml.feature import VectorAssembler

import config
from model_prediction import predict


# Create a Spark session
spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()


# Define the schema of your CSV file
csvSchema = StructType([
    StructField("AT", DoubleType(), True),
    StructField("V", DoubleType(), True),
    StructField("AP", DoubleType(), True),
    StructField("RH", DoubleType(), True),
    # Add more fields as needed
])

# Define the path to the folder where the CSV files will be uploaded
folderPath = "/Users/i741961/Documents/HKA/Big_Data/BigData/files/streaming"

# Read the CSV files as a streaming DataFrame
csvStreamDF = (
    spark
    .readStream
    .option("header", "true")
    .option("sep", "|")
    .schema(csvSchema)
    .csv(folderPath)
)

assembler = VectorAssembler(inputCols=["AT", "V", "AP", "RH"], outputCol="features")
assembledDF = assembler.transform(csvStreamDF)
resultDF = predict(assembledDF)

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
