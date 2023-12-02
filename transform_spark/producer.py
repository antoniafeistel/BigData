import findspark
findspark.init()

from config import config
import re
import hashlib
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType, IntegerType, LongType, StringType, StructField, StructType


def extract_number_from_string(input_string):
    # Verwende einen regulären Ausdruck, um die Nummer aus dem String zu extrahieren
    match = re.search(r'\d+', input_string)
    
    # Überprüfe, ob eine Übereinstimmung gefunden wurde
    if match:
        return int(match.group())
    else:
        return 25
    

# Funktion zum Hashen von Strings für die Encodierung
def hash_int(input_string):
    # Hier wird ein einfacher MD5-Hash verwendet, du kannst auch andere Hash-Algorithmen verwenden
    hash_object = hashlib.md5(input_string.encode())
    hex_hash = hash_object.hexdigest()

    # Extrahiere die unteren 8 Bytes des Hexadezimal-Hash-Werts und interpretiere sie als Integer
    hash_int = int(hex_hash[-5:], 16)

    return hash_int


hash_udf = udf(lambda input_string: hash_int(input_string), IntegerType())

spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()

schema = StructType([
    StructField("ssn", StringType(), True),
    StructField("cc_num", StringType(), True),
    StructField("first", StringType(), True),
    StructField("last", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("street", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("zip", IntegerType(), True),
    StructField("lat", DoubleType(), True),
    StructField("long", DoubleType(), True),
    StructField("city_pop", IntegerType(), True),
    StructField("job", StringType(), True),
    StructField("dob", StringType(), True),
    StructField("acct_num", LongType(), True),
    StructField("profile", StringType(), True),
    StructField("trans_num", StringType(), True),
    StructField("trans_date", StringType(), True),
    StructField("trans_time", StringType(), True),
    StructField("unix_time", LongType(), True),
    StructField("category", StringType(), True),
    StructField("amt", DoubleType(), True),
    StructField("is_fraud", IntegerType(), True),
    StructField("merchant", StringType(), True),
    StructField("merch_lat", DoubleType(), True),
    StructField("merch_long", DoubleType(), True)
])

relevant_columns = ["gender", "state", "city_pop", "job", "profile", "trans_date", "unix_time", "category", "amt", "merchant"]


# Create Streaming dataframe
streamingDataFrame = spark. \
            readStream. \
            option("header", "true"). \
            option("sep", "|"). \
            schema(schema). \
            csv(config.INPUT_FOLDER)

# encode dataframe
encodedDataFrame = streamingDataFrame.withColumns({
   "gender": hash_udf(streamingDataFrame.gender),
    "state": hash_udf(streamingDataFrame.state),
    "job": hash_udf(streamingDataFrame.job),
    "profile": hash_udf(streamingDataFrame.profile),
    "trans_date": hash_udf(streamingDataFrame.trans_time),
    "category": hash_udf(streamingDataFrame.category),
    "merchant": hash_udf(streamingDataFrame.merchant)
})

encodedDataFrame = encodedDataFrame.select(relevant_columns)

query_kafka = (
    encodedDataFrame.selectExpr("to_json(struct(*)) AS value")
    .writeStream
    .format("kafka")
    .outputMode("append")
    .option("kafka.bootstrap.servers", config.KAFKA_BOOTSTRAP_SERVERS)
    .option("topic", config.KAFKA_TOPIC)
    .option("checkpointLocation", config.KAFKA_CHECKPTS_PATH)
    .start()
)

query_kafka.awaitTermination()
