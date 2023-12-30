import os
from dotenv import load_dotenv
from pyspark.sql.types import DoubleType, IntegerType, LongType, StringType, StructField, StructType
from pyspark.sql.functions import udf
from hashlib import md5


# lowest bytes to be extracted to construct the integer hash value
lowest_bytes = -5
# base of the hashed number
base = 16


CSV_SEP = "|"
CSV_HEADER = "true"
FEATURES_COL = "features"
LABEL_COL = "is_fraud"
PREDICTION_COL = "prediction"
WEIGHT_COL = "weight"

config_dir_path = os.path.dirname(os.path.abspath(__file__))
repo_dir_path = os.path.join(config_dir_path, os.pardir)
# here defined to avoid circular import problems
ENV_VARS_PATH = os.path.join(repo_dir_path, "scripts", ".env")
load_dotenv(ENV_VARS_PATH)
VERSION = os.getenv("DATA_VERSION")

features = ["gender", "state", "city_pop", "job", "profile", "trans_date", "unix_time", "category", "amt", "merchant"]


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


def hash_str(cat_feature_val):
    hash_object = md5(cat_feature_val.encode())
    hex_hash = hash_object.hexdigest()

    # extract the lowest bytes of the hex hash value in string representation as integer
    hash_int = int(hex_hash[lowest_bytes:], base)

    return hash_int


hash_udf = udf(lambda cat_feature_val: hash_str(cat_feature_val), IntegerType())


def encode_df(df):
    return df.withColumns({
        "gender": hash_udf(df.gender),
        "state": hash_udf(df.state),
        "job": hash_udf(df.job),
        "profile": hash_udf(df.profile),
        "trans_date": hash_udf(df.trans_time),
        "category": hash_udf(df.category),
        "merchant": hash_udf(df.merchant)
    })
