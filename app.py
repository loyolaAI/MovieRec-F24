# app.py
from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

# Load your machine learning model
model = joblib.load("model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    prediction = model.predict([data["input"]])  # Adjust based on your input format
    return jsonify({"prediction": prediction.tolist()})


if __name__ == "__main__":
    app.run(debug=True)
