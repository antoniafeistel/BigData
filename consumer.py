from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

import config


def consume_and_append_to_spark(spark, kafka_topic, bootstrap_servers):
    schema = StructType([
        StructField("field1", StringType(), True),
        StructField("field2", IntegerType(), True),
        # Add more fields based on your CSV columns
    ])

    # Read messages from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse JSON message value
    parsed_df = df.selectExpr("CAST(value AS STRING)").select(from_json("value", schema).alias("data")).select("data.*")
    parsed_df.printSchema()

    # Append to Spark DataFrame
    # You can further process or write this DataFrame as needed
    final_df = parsed_df \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    final_df.awaitTermination()


curr_spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()

consume_and_append_to_spark(curr_spark, config.KAFKA_TOPIC, config.KAFKA_BOOTSTRAP_SERVERS)
