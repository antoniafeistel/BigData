from pyspark.ml import Pipeline

from config import config
from pyspark.sql import SparkSession
from config.config import schema, relevant_columns, hash_udf
from pyspark.ml.feature import StringIndexer, VectorIndexer, IndexToString
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SQLContext
from rf_clf_model.model import train_rf_clf_model, save_model


spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()
import os
print("heeeeeelloo")
print(os.path.exists(config.INPUT_FOLDER_RAW))
dataFrame = spark.read.csv(config.INPUT_FOLDER_RAW, header=True, sep='|', schema=schema)

#indexers = [StringIndexer(inputCol=column, outputCol=column).fit(dataFrame) for column in relevant_columns ]






#pipeline = Pipeline(stages=indexers)
#df_r = pipeline.fit(dataFrame).transform(dataFrame)

#dataFrame.show()


encodedDataFrame = dataFrame.withColumns({
   "gender": hash_udf(dataFrame.gender),
    "state": hash_udf(dataFrame.state),
    "job": hash_udf(dataFrame.job),
    "profile": hash_udf(dataFrame.profile),
    "trans_date": hash_udf(dataFrame.trans_time),
    "category": hash_udf(dataFrame.category),
    "merchant": hash_udf(dataFrame.merchant)
})

encodedDataFrame.show()

assembler = VectorAssembler(inputCols=relevant_columns, outputCol="features")
df2 = assembler.transform(encodedDataFrame)
df_train = df2.select("features", "is_fraud")

rf_clf_model = train_rf_clf_model(df_train)
save_model(rf_clf_model, config.MODEL_PATH)
