import warnings

warnings.filterwarnings("ignore")

import json
import numpy as np
import pandas as pd
import mlflow
import xgboost as xgb
import shap
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score

from evidently import Report
from evidently.presets import DataDriftPreset

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from lib.spark_session import get_spark


def main():
    print("--- 1. FEATURE ENGINEERING (Reading from Gold) ---")
    spark = get_spark("ml_churn", iceberg=True)

    # SILENCE VERBOSE JVM/SPARK LOGS IMMEDIATELY
    spark.sparkContext.setLogLevel("ERROR")

    # Read the Gold customer_360 table into Pandas
    df = spark.table("lake.gold.customer_360").toPandas()

    # Create synthetic churn target: churned if recency > 60 days
    df["churned"] = (df["recency_days"] > 60).astype(int)

    features = ["recency_days", "frequency", "monetary"]
    X = df[features]
    y = df["churned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training data shape: {X_train.shape}. Churn rate: {y.mean():.2%}")

    print("--- 2. MODEL TRAINING & MLFLOW TRACKING ---")
    mlflow.set_tracking_uri("sqlite:////home/sbaker/MegaMart/mlflow.db")
    mlflow.set_experiment("Customer_Churn_Prediction")

    with mlflow.start_run():
        params = {
            "objective": "binary:logistic",
            "device": "cuda",  # Leverages your RTX 3060 GPU
            "max_depth": 5,
            "learning_rate": 0.1,
            "eval_metric": "aucpr",
        }
        mlflow.log_params(params)

        dtrain = xgb.DMatrix(X_train, label=y_train)
        dtest = xgb.DMatrix(X_test, label=y_test)

        model = xgb.train(params, dtrain, num_boost_round=100)

        preds = model.predict(dtest)
        auc = roc_auc_score(y_test, preds)
        pr_auc = average_precision_score(y_test, preds)

        mlflow.log_metric("roc_auc", auc)
        mlflow.log_metric("pr_auc", pr_auc)
        print(f"Model trained! ROC AUC: {auc:.4f} | PR AUC: {pr_auc:.4f}")

        mlflow.xgboost.log_model(model, name="xgb_churn_model")

        print("--- 3. EXPLAINABILITY (SHAP) ---")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
        mean_abs_shap = np.abs(shap_values).mean(axis=0)

        for i, feat in enumerate(features):
            mlflow.log_metric(f"shap_importance_{feat}", mean_abs_shap[i])
            print(f"Feature Importance ({feat}): {mean_abs_shap[i]:.4f}")

    print("--- 4. BATCH SCORING TO ICEBERG ---")
    df["churn_probability"] = model.predict(xgb.DMatrix(X))

    scores_df = spark.createDataFrame(df[["customer_id", "churn_probability"]])
    scores_df.writeTo("lake.gold.customer_churn_scores").using("iceberg").createOrReplace()
    print("Scores written to lake.gold.customer_churn_scores")

    print("--- 5. DRIFT MONITORING (EVIDENTLY & PROMETHEUS) ---")
    ref_data = X_train.copy()
    cur_data = X_test.copy()

    report = Report([DataDriftPreset()])
    eval_res = report.run(current_data=cur_data, reference_data=ref_data)

    # Extract dict safely across Evidently object structures
    target_obj = eval_res if eval_res is not None else report
    if hasattr(target_obj, "dict"):
        result = target_obj.dict()
    elif hasattr(target_obj, "as_dict"):
        result = target_obj.as_dict()
    elif hasattr(target_obj, "json"):
        result = json.loads(target_obj.json())
    else:
        result = {}

    reg = CollectorRegistry()
    g = Gauge(
        "megamart_feature_psi",
        "data drift (PSI) per feature",
        ["feature"],
        registry=reg,
    )

    drift_data = {}
    if isinstance(result, dict):
        for metric in result.get("metrics", []):
            res = metric.get("result", {})
            if "drift_by_columns" in res:
                drift_data = res["drift_by_columns"]
                break

    for feat in features:
        score = 0.0
        if feat in drift_data:
            score = drift_data[feat].get("drift_score", 0.0)
        g.labels(feature=feat).set(score)
        print(f"Drift - {feat}: {score:.4f}")

    try:
        push_to_gateway("localhost:9091", job="megamart_drift", registry=reg)
        print("Successfully pushed drift metrics to Prometheus Pushgateway!")
    except Exception as e:
        print(f"Warning: Could not push to Pushgateway (is Docker running?): {e}")

    spark.stop()


if __name__ == "__main__":
    main()