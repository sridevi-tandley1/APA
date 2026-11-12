"""Train a tiny salary model and log + register it in MLflow.

Tracking uses a local SQLite file (mlflow.db). Recent MLflow releases refuse
the old ./mlruns file store, so do not switch back to a file:// URI.
"""
import os

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

DATA_PATH = "data.csv"
FEATURES = ["experience_years"]
MODEL_NAME = "salary_model"
EXPERIMENT = "apa-salary-demo"
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")


def load_data(path=DATA_PATH):
    return pd.read_csv(path)


def train_and_log():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)
    df = load_data()
    X, y = df[FEATURES].astype(float), df["salary"]  # float avoids an MLflow schema warning
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    with mlflow.start_run(run_name="linear-salary-model"):
        fit_intercept = True
        mlflow.log_param("fit_intercept", fit_intercept)
        model = LinearRegression(fit_intercept=fit_intercept).fit(X_train, y_train)
        mse = mean_squared_error(y_test, model.predict(X_test))
        mlflow.log_metric("mse", mse)
        # log the model and register a new version in the model registry
        mlflow.sklearn.log_model(model, name=MODEL_NAME,
                                 registered_model_name=MODEL_NAME,
                                 input_example=X_train.head(2))
        print("Trained, logged MSE:", round(mse, 2))
        return model


if __name__ == "__main__":
    train_and_log()
