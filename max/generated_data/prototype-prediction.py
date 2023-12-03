
import findspark
findspark.init("/usr/local/spark-3.5.0-bin-hadoop3")
import pyspark

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

import kafka_streaming.model_training
from kafka_streaming.model_prediction import predict

import sys

def proceed_prediction(file_path, dataFrame):
    print("Processing file: {file_path}")
    spark = SparkSession.builder.master("spark://N279WMVDJ2:7077").getOrCreate()
    # Initialisiere die Spark-Sitzung
    #spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

    # Lade das CSV-Datei in ein DataFrame
    #dataFrame = spark.read.csv(file_path, header=True, inferSchema=True, sep='|')

    feature_cols = [ 'cc_num', "lat", "long" ]

    #feature_cols.remove("is_fraud")  # Entferne die Label-Spalte
    vector_assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    dataFrame = vector_assembler.transform(dataFrame)

    model_path = "max/generated_data/model"

    loaded_model = RandomForestClassificationModel.load(model_path)

    predictions = predict(dataFrame)

    predictions.show()

    #dataFrame.drop(index=[0, 1])



if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        print("No file path provided.")