import os

from flask import Flask, request
from gliner import GLiNER
from waitress import serve

__version__ = "1.2.0"

app = Flask(__name__)

print("Starting ph-eye version " + __version__)
model_name = os.getenv("MODEL_NAME", "philterd/ph-eye-pii-base")
print("Using model " + model_name)
model = GLiNER.from_pretrained(model_name)
print("Model loaded")

@app.route("/status", methods=["GET"])
def status():
    return "healthy: " + model_name


@app.route("/find", methods=["POST"])
def find():

    try:

        r = request.json

        text = r["text"]
        labels = ["Person"] if "labels" not in r else r["labels"]
        threshold = 0.5 if "threshold" not in r else r["threshold"]

        if len(labels) == 0:
            labels = ["Person"]

        entities = model.predict_entities(text, labels, threshold=threshold)

        return entities, 200

    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)

