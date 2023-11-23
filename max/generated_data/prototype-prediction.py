
import findspark
findspark.init("/usr/local/spark-3.5.0-bin-hadoop3")
import pyspark

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

import sys

def main(file_path):
    print("Processing file: {file_path}")
    spark = SparkSession.builder.master("spark://JVVWXW05C9:7077").getOrCreate()
    # Initialisiere die Spark-Sitzung
    #spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

    # Lade das CSV-Datei in ein DataFrame
    dataFrame = spark.read.csv(file_path, header=True, inferSchema=True, sep='|')

    model_path = "/model"

    loaded_model = RandomForestClassificationModel.load(model_path)

    predictions = loaded_model.transform(dataFrame)

    print(predictions)

    dataFrame.drop(index=[0, 1])



if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        print("No file path provided.")