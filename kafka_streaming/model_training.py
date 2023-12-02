from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
import pandas as pd

from config import config


spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()
file_path = '/Users/i741961/Documents/HKA/Big_Data/BigData/files/training_data/train.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet2')
feature_columns = list(df.columns[:-1])

assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
df = SQLContext(spark).createDataFrame(df)
df2 = assembler.transform(df)
df_train = df2.select("features", "is_fraud")

train, test = df_train.randomSplit([0.7, 0.3])

lr = LinearRegression(featuresCol="features", labelCol="is_fraud", predictionCol="prediction")
model = lr.fit(train)

predictions = model.transform(test)
predictions.show()

model.write().overwrite().save(config.MODEL_PATH)
