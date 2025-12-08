# model_utils.py
import mlflow
import mlflow.sklearn
import os

MLFLOW_TRACKING_DIR = os.path.abspath("mlruns")
mlflow.set_tracking_uri(f"file://{MLFLOW_TRACKING_DIR}")

def load_latest_model(model_name="salary_model"):
    # Find latest run that logged a model artifact with given path
    client = mlflow.tracking.MlflowClient(tracking_uri=f"file://{MLFLOW_TRACKING_DIR}")
    runs = client.search_runs(experiment_ids=["0"], order_by=["start_time DESC"], max_results=50)
    for run in runs:
        # check if artifact with path exists
        artifacts = client.list_artifacts(run.info.run_id, path="salary_model")
        if artifacts:
            model_uri = f"runs:/{run.info.run_id}/salary_model"
            model = mlflow.sklearn.load_model(model_uri)
            return model
    raise FileNotFoundError("No logged model found in local mlruns/")