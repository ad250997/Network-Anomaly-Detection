from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

BIN_MODEL_PATH = "artifacts/binary_model.joblib"
MULTI_MODEL_PATH = "artifacts/multiclass_model.joblib"

bin_model = joblib.load(BIN_MODEL_PATH)
multi_model = joblib.load(MULTI_MODEL_PATH)

def scores_to_confidence(scores, classes):
    """
    Convert LinearSVC decision scores to normalized confidence values.
    These are NOT true probabilities.
    """
    exp_scores = np.exp(scores - np.max(scores))  # numerical stability
    conf = exp_scores / exp_scores.sum()
    return dict(zip(classes, conf))

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
    scores = multi_model.decision_function(X)[0]
    classes = multi_model.classes_
    attack_type_confidence = scores_to_confidence(scores, classes)


    return {
        "prediction": "attack",
        "attack_probability": round(float(attack_prob),8),
        "attack_type": attack_type,
        "attack_type_confidence": {
            k: round(float(v),8) for k, v in attack_type_confidence.items()
        },
        "note": "attack_type_confidence represents normalized model confidence, not true probability"
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
