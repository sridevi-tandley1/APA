"""Load the newest registered version of the model for serving."""
import os

import mlflow
import mlflow.sklearn

MODEL_NAME = "salary_model"
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")


def load_latest_model(model_name=MODEL_NAME):
    mlflow.set_tracking_uri(TRACKING_URI)
    try:
        return mlflow.sklearn.load_model(f"models:/{model_name}/latest")
    except Exception as exc:  # no registered version yet
        raise FileNotFoundError(
            f"No registered '{model_name}' model found. Run `python train.py` first."
        ) from exc
