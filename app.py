"""Flask prediction API for the salary model."""
import os

import pandas as pd
from flask import Flask, jsonify, request

from model_utils import load_latest_model
from train import FEATURES

app = Flask(__name__)
model = None


def get_model():
    global model
    if model is None:
        model = load_latest_model()
    return model


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)  # None for a missing or non-JSON body
    if not isinstance(data, dict):
        return jsonify({"error": "send a JSON object"}), 400
    # Accept {"experience_years": 4} or {"instances": [[4], [6]]}
    if "instances" in data:
        rows = data["instances"]
    elif "experience_years" in data:
        rows = [[data["experience_years"]]]
    else:
        return jsonify({"error": "invalid payload"}), 400
    try:
        X = pd.DataFrame(rows, columns=FEATURES, dtype=float)
    except (ValueError, TypeError):
        return jsonify({"error": "each instance must be one number: [experience_years]"}), 400
    try:
        m = get_model()
    except FileNotFoundError as exc:
        return jsonify({"error": "model not available", "detail": str(exc)}), 503
    return jsonify({"predictions": m.predict(X).tolist()}), 200


if __name__ == "__main__":
    # development server only; in Docker the image runs gunicorn instead
    app.run(host="127.0.0.1", port=8000, debug=os.getenv("FLASK_DEBUG") == "1")
