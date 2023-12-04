import findspark
findspark.init()

from config import config
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler


spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()
# Initialisiere die Spark-Sitzung
#spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

csv_file_path = './max/generated_data/data/adults_50up_female_rural_4-5_example.csv'

# Lade das CSV-Datei in ein DataFrame
dataFrame = spark.read.csv(csv_file_path, header=True, inferSchema=True, sep='|')
#featuresCol = list(dataFrame.columns[:-1])
featuresCol = ["cc_num", "lat", "long"]

#feature_cols.remove("is_fraud")  # Entferne die Label-Spalte

vector_assembler = VectorAssembler(inputCols=featuresCol, outputCol="features")
# dataFrame = SQLContext(spark).createDataFrame(dataFrame)
dataFrame = vector_assembler.transform(dataFrame)
dataFrame = dataFrame.select("features", "is_fraud")

rf = RandomForestClassifier(labelCol="is_fraud", featuresCol="features", predictionCol="prediction", numTrees=10)
model = rf.fit(dataFrame)

# Zeige das Modell und dessen Einstellungen
rfModel = model.trees
print(rfModel)  # summary only

model.write().overwrite().save(config.MODEL_PATH)

