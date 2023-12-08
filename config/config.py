INPUT_FOLDER_RAW = 'resources/data/raw'
INPUT_FOLDER_TEST = 'resources/data/test'
OUTPUT_FOLDER = '/resources/data/train'
TRAIN_DATA_PATH = '/resources/data/train'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'bigDataTest'
CSV_FILE_PATH = '/files/test.csv'
AVRO_FILE_PATH = '/files/test.avro'
SPARK_MASTER = "spark://LFK66VG60V:7077"
MODEL_PATH = 'resources/model'
KAFKA_CHECKPTS_PATH = 'kafka_checkpoints'


from pyspark.sql.functions import udf
import hashlib
from pyspark.sql.types import DoubleType, IntegerType, LongType, StringType, StructField, StructType

relevant_columns = ["gender", "state", "city_pop", "job", "profile", "trans_date", "unix_time", "category", "amt", "merchant"]

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

def hash_int(input_string):
    # Hier wird ein einfacher MD5-Hash verwendet, du kannst auch andere Hash-Algorithmen verwenden
    hash_object = hashlib.md5(input_string.encode())
    hex_hash = hash_object.hexdigest()

    # Extrahiere die unteren 8 Bytes des Hexadezimal-Hash-Werts und interpretiere sie als Integer
    hash_int = int(hex_hash[-5:], 16)

    return hash_int


hash_udf = udf(lambda input_string: hash_int(input_string), IntegerType())
