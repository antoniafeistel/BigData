import findspark
findspark.init("/usr/local/spark-3.5.0-bin-hadoop3")

from config import config
from pyspark.ml.classification import RandomForestClassificationModel

loaded = False
model = None


def proceed_prediction(dataFrame):
    global loaded, model
    if not loaded:
        model = RandomForestClassificationModel.load(config.MODEL_PATH)
        loaded = True
    prediction = model.transform(dataFrame)
    return prediction
