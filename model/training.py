import findspark
findspark.init()

from config import config
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler


def train_model(df_train):
    rf = RandomForestClassifier(labelCol="is_fraud", featuresCol="features", predictionCol="prediction", numTrees=10)
    model = rf.fit(df_train)

    # Zeige das Modell und dessen Einstellungen
    rfModel = model.trees
    print(rfModel)  # summary only

    model.write().overwrite().save(config.MODEL_PATH)

