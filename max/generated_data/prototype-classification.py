import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


spark = SparkSession.builder.master("spark://N279WMVDJ2:7077").getOrCreate()
# Initialisiere die Spark-Sitzung
#spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

csv_file_path = './generated_data/adults_50up_female_urban_6-7.csv'

# Lade das CSV-Datei in ein DataFrame
dataFrame = spark.read.csv(csv_file_path, header=True, inferSchema=True, sep='|')

feature_cols = [ 'cc_num', "lat", "long" ]

#feature_cols.remove("is_fraud")  # Entferne die Label-Spalte
vector_assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
dataFrame = vector_assembler.transform(dataFrame)

# Aufteilung der Daten in Trainings- und Testsets
(trainingData, testData) = dataFrame.randomSplit([0.7, 0.3])

rf = RandomForestClassifier(labelCol="is_fraud", featuresCol="features", numTrees=10)
model = rf.fit(trainingData)

# Mache Vorhersagen
predictions = model.transform(testData)

# Evaluierung des Modells
evaluator = MulticlassClassificationEvaluator(
    labelCol="is_fraud", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Accuracy = %g" % accuracy)

# Zeige das Modell und dessen Einstellungen
rfModel = model.trees
print(rfModel)  # summary only

spark.stop()