from dotenv import load_dotenv
load_dotenv()
from git import Repo
from database.models.model_improvements import ModelImprovements
from database.models.champion_model import ChampionModel
from database.mongo import mongo_collection
from xgboost import XGBClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss
from sklearn.datasets import load_iris
import mlflow
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import MlflowMetrics

def calculate_percentage_difference(new_value, old_value):
    if old_value == 0:
        return float('inf') if new_value > 0 else 0
    return ((new_value - old_value) / old_value) * 100

db: Session = next(get_db())

champion_model = db.query(ChampionModel).filter(ChampionModel.is_active == True).first()
mlflow_metrics = db.query(MlflowMetrics).filter(MlflowMetrics.run_id == champion_model.run_id and MlflowMetrics.experiment_id == champion_model.experiment_id).first()

iris = load_iris()
X, y = iris.data, iris.target

np.random.shuffle(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_bad = np.random.rand(*X_train.shape)
X_test_bad = np.random.rand(*X_test.shape)

model = XGBClassifier(n_estimators=10, max_depth=2, learning_rate=0.1, use_label_encoder=False, eval_metric="mlogloss")
params = model.get_params()

model_name = "XGBoost"
mlflow.set_experiment("Experiment for XGBoost")
with mlflow.start_run():
    try:
        experiment_id = mlflow.active_run().info.experiment_id
        run_id = mlflow.active_run().info.run_id    

        model.fit(X_train_bad, y_train) 
        y_pred = model.predict(X_test_bad)
        y_pred_prob = model.predict_proba(X_test_bad)

        acc = 0.83 #accuracy_score(y_test, y_pred)
        f1 = 0.325 #f1_score(y_test, y_pred, average="macro")
        precision = 0.19 # precision_score(y_test, y_pred, average="macro", zero_division=0)
        recall = 0.39 #recall_score(y_test, y_pred, average="macro", zero_division=0)
        logloss = 0.39 #log_loss(y_test, y_pred_prob)

        mlflow.log_param("model_type", model_name)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("log_loss", logloss)

        improvements = {
            "accuracy":  calculate_percentage_difference(acc, mlflow_metrics.accuracy),
            "f1_score":  calculate_percentage_difference(f1, mlflow_metrics.f1_score),
            "precision": calculate_percentage_difference(precision, mlflow_metrics.precision),
            "recall":    calculate_percentage_difference(recall, mlflow_metrics.recall),
            "log_loss":  calculate_percentage_difference(logloss, mlflow_metrics.log_loss),
        }
        repo = Repo()

        mongo_doc = mongo_collection.insert_one(params)
        mongo_id = str(mongo_doc.inserted_id)

        g_commit = str(repo.head.commit)
        new_metric = MlflowMetrics(
            experiment_id=experiment_id,
            run_id=run_id,
            model="XGBoost",
            accuracy=acc,
            recall=recall,
            precision=precision,
            f1_score=f1,
            log_loss=logloss,
            mongo_id=mongo_id,
            commit_hash=g_commit
        )
        db.add(new_metric)
        db.commit()

        impr = ModelImprovements(
            commit_hash=g_commit,
            experiment_id=experiment_id,
            run_id=run_id,
            percentage_change_accuracy = calculate_percentage_difference(acc, mlflow_metrics.accuracy),
            percentage_change_recall = calculate_percentage_difference(f1, mlflow_metrics.f1_score),
            percentage_change_precision = calculate_percentage_difference(precision, mlflow_metrics.precision),
            percentage_change_f1 = calculate_percentage_difference(recall, mlflow_metrics.recall),
            percentage_change_log_loss = calculate_percentage_difference(logloss, mlflow_metrics.log_loss),
        )

        db.add(impr)
        db.commit()
    except:
        db.rollback()
        raise Exception
    print(improvements)

    

