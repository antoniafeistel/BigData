from pyspark.ml.classification import RandomForestClassifier


def train_rf_clf_model(df_train):
    rf_clf = RandomForestClassifier(labelCol="is_fraud", featuresCol="features", predictionCol="prediction", numTrees=10)
    rf_clf_model = rf_clf.fit(df_train)
    print(rf_clf_model.trees)
    return rf_clf_model


def save_model(model, path):
    model.write().overwrite().save(path)
