import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()
from database.mongo import mongo_collection
from xgboost import XGBClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss
from sklearn.datasets import load_iris
import mlflow

iris = load_iris()
X, y = iris.data, iris.target

np.random.shuffle(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_bad = np.random.rand(*X_train.shape)
X_test_bad = np.random.rand(*X_test.shape)

model = XGBClassifier(n_estimators=10, max_depth=2, learning_rate=0.1, use_label_encoder=False, eval_metric="mlogloss")
params = model.get_params()

model_name = "XGBoost"

with mlflow.start_run():
    experiment_id = mlflow.active_run().info.experiment_id
    run_id = mlflow.active_run().info.run_id

    model.fit(X_train_bad, y_train)
    y_pred = model.predict(X_test_bad)
    y_pred_prob = model.predict_proba(X_test_bad)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")
    precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
    recall = recall_score(y_test, y_pred, average="macro", zero_division=0)
    logloss = log_loss(y_test, y_pred_prob)

    mlflow.log_param("model_type", model_name)
    mlflow.log_metric("accuracy", 0.5) # manipulate this to find impact on the model
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("log_loss", logloss)

    mongo_doc = mongo_collection.insert_one(params)
    mongo_id = str(mongo_doc.inserted_id)