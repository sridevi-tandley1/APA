import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn
import os

DATA_PATH = "data.csv"
MLFLOW_TRACKING_DIR = os.path.abspath("mlruns")  # local
mlflow.set_tracking_uri(f"file://{MLFLOW_TRACKING_DIR}")

def load_data(path=DATA_PATH):
    return pd.read_csv(path)

def train_and_log():
    df = load_data()
    X = df[["experience_years"]]
    y = df["salary"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.3)

    with mlflow.start_run(run_name="linear-salary-model"):
        # hyperparams
        fit_intercept = True
        mlflow.log_param("fit_intercept", fit_intercept)

        model = LinearRegression(fit_intercept=fit_intercept)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        mlflow.log_metric("mse", mse)

        # save model into MLflow (this registers artifact under mlruns/...)
        mlflow.sklearn.log_model(model, "salary_model")

        print("Trained, logged MSE:", mse)
        return model

if __name__ == "__main__":
    train_and_log()