from flask import Flask, request, jsonify
import joblib
import pandas as pd

BIN_MODEL_PATH = "artifacts/binary_model.joblib"
MULTI_MODEL_PATH = "artifacts/multiclass_model.joblib"

bin_model = joblib.load(BIN_MODEL_PATH)
multi_model = joblib.load(MULTI_MODEL_PATH)

def predict_single(record: dict):
    """
    record: dict of raw feature values
    """
    X = pd.DataFrame([record])

    attack_pred = bin_model.predict(X)[0]
    attack_prob = bin_model.predict_proba(X)[0, 1]

    if attack_pred == 0:
        return {
            "prediction": "normal",
            "attack_probability": float(attack_prob)
        }

    attack_type = multi_model.predict(X)[0]

    return {
        "prediction": "attack",
        "attack_type": attack_type,
        "attack_probability": float(attack_prob)
    }

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        result = predict_single(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
