import findspark
findspark.init()

import pyspark
from config import config
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()
# Initialisiere die Spark-Sitzung
#spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

csv_file_path = './max/generated_data/adults_50up_female_urban_6-7.csv'

# Lade das CSV-Datei in ein DataFrame
dataFrame = spark.read.csv(csv_file_path, header=True, inferSchema=True, sep='|')
feature_columns = list(dataFrame.columns[:-1])

#feature_cols.remove("is_fraud")  # Entferne die Label-Spalte

vector_assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df = SQLContext(spark).createDataFrame(dataFrame)
dataFrame = vector_assembler.transform(dataFrame)
dataFrame = dataFrame.select("features", "is_fraud")

rf = RandomForestClassifier(labelCol="is_fraud", featuresCol="features", predictionCol="prediction", numTrees=10)
model = rf.fit(dataFrame)

# Evaluierung des Modells
evaluator = MulticlassClassificationEvaluator(
    labelCol="is_fraud", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Accuracy = %g" % accuracy)

# Zeige das Modell und dessen Einstellungen
rfModel = model.trees
print(rfModel)  # summary only

model.write().overwrite().save(config.MODEL_PATH)

