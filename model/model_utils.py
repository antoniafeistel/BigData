from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel

from config import data_handling, path_handling


# number of trees for random forest classifier
num_trees = 10
loaded = False
model = None


def train_model(df_train):
    rf_clf = RandomForestClassifier(labelCol=data_handling.LABEL_COL, featuresCol=data_handling.FEATURES_COL, predictionCol=data_handling.PREDICTION_COL, numTrees=num_trees)
    rf_clf_model = rf_clf.fit(df_train)
    return rf_clf_model


def save_model(trained_model, path):
    trained_model.write().overwrite().save(path)


def predict(streaming_df):
    global loaded, model
    if not loaded:
        model = RandomForestClassificationModel.load(path_handling.MODEL_PATH)
        loaded = True
    predicted_df = model.transform(streaming_df)
    return predicted_df
