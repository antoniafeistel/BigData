import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


spark = SparkSession.builder.master("spark://N279WMVDJ2:7077").getOrCreate()

### für alle csv.files in dem folder außer customer.csv
### mache nimm alle daten und füge sie dem data frame hinzu
### danach 