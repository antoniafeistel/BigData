from pyspark.sql import SparkSession

from config import path_handling, data_handling


spark = SparkSession.builder.master(path_handling.SPARK_MASTER).getOrCreate()


streaming_df = (spark.
                readStream.
                option("header", data_handling.CSV_HEADER).
                option("sep", data_handling.CSV_SEP).
                schema(data_handling.schema).
                csv(path_handling.INPUT_FOLDER_TEST)
                )

encoded_df = data_handling.encode_df(streaming_df)
selected_df = encoded_df.select(data_handling.features)

query_kafka = (
    selected_df.selectExpr("to_json(struct(*)) AS value")
    .writeStream
    .format("kafka")
    .outputMode("append")
    .option("kafka.bootstrap.servers", path_handling.KAFKA_BOOTSTRAP_SERVERS)
    .option("topic", path_handling.KAFKA_TOPIC)
    .option("checkpointLocation", path_handling.KAFKA_CHECKPTS_PATH)
    .start()
)

query_kafka.awaitTermination()
