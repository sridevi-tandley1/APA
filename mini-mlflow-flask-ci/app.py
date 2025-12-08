# app.py
from flask import Flask, request, jsonify
from model_utils import load_latest_model

app = Flask(__name__)

# Load model once at startup (fast locally)
model = None
try:
    model = load_latest_model()
    print("Model loaded at startup.")
except Exception as e:
    print("Warning: could not load model at startup:", e)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    global model
    if model is None:
        try:
            model = load_latest_model()
        except Exception as e:
            return jsonify({"error": "model not available", "detail": str(e)}), 500

    data = request.json
    # Accept {"experience_years": 4} or {"instances": [[4], [6]]}
    if "instances" in data:
        X = data["instances"]
    elif "experience_years" in data:
        X = [[data["experience_years"]]]
    else:
        return jsonify({"error": "invalid payload"}), 400

    preds = model.predict(X).tolist()
    return jsonify({"predictions": preds}), 200

if __name__ == "__main__":
    # for dev only
    app.run(host="0.0.0.0", port=8000, debug=True)