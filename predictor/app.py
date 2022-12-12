from flask import Flask, jsonify, request
from model.model import Predictor

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "ok"})

@app.route("/predict/", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        photo = data["photo"]
        resp = predictor(photo)
        return jsonify({"status": "ok", "resp": resp})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


predictor = Predictor()