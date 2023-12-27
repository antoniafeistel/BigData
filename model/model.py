from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel

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


def train_rf_clf_model(df_train):
    rf_clf = RandomForestClassifier(labelCol="is_fraud", featuresCol="features", predictionCol="prediction", numTrees=10)
    rf_clf_model = rf_clf.fit(df_train)
    print(rf_clf_model.trees)
    return rf_clf_model


def save_model(model, path):
    model.write().overwrite().save(path)
