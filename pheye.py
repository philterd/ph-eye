import os

from flask import Flask, request
from gliner import GLiNER
from numpy.compat import os_fspath

__version__ = "1.0.0"

app = Flask(__name__)

model_name = os.getenv("MODEL_NAME", "urchade/gliner_mediumv2.1")
model = GLiNER.from_pretrained(model_name)

@app.route("/status", methods=["GET"])
def status():
    return "healthy: " + model_name


@app.route("/find", methods=["POST"])
def find():

    r = request.json
    text = r["text"]
    threshold = r["threshold"]
    labels = r["labels"]

    if len(labels) == 0:
        labels = ["Person"]

    entities = model.predict_entities(text, labels, threshold=threshold)

    return entities, 200

if __name__ == "__main__":
    app.run()
