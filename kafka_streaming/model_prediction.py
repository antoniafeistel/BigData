from pyspark.ml.regression import LinearRegressionModel

import config


loaded = False
model = None


def predict(streaming_df):
    global loaded, model
    if not loaded:
        model = LinearRegressionModel.load(config.MODEL_PATH)
        loaded = True
    prediction = model.transform(streaming_df)
    return prediction
