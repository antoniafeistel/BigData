from pyspark.ml.classification import RandomForestClassificationModel

from config import config


loaded = False
model = None


def predict(streaming_df):
    global loaded, model
    if not loaded:
        model = RandomForestClassificationModel.load(config.MODEL_PATH)
        loaded = True
    prediction = model.transform(streaming_df)
    return prediction
