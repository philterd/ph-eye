import os

from flask import Flask, request, jsonify
from gliner import GLiNER
from transformers import pipeline
from waitress import serve

__version__ = "1.2.3"

app = Flask(__name__)

print("Starting ph-eye version " + __version__)
model_name = os.getenv("MODEL_NAME", "philterd/ph-eye-pii-base")
print("Using model " + model_name)
model = GLiNER.from_pretrained(model_name)
print("Model loaded and ready to serve requests")

# Initialize the Medical NER pipeline
print("Loading model...")
medical_ner_pipeline = pipeline("token-classification", model="blaze999/Medical-NER", aggregation_strategy="simple")
print("Model loaded successfully!")


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
        medical_conditions = extract_medical_conditions(text)

        all_entities = entities + medical_conditions

        return all_entities, 200

    except Exception as e:
        print(str(e))
        return str(e), 500


def extract_medical_conditions(text):

    results = medical_ner_pipeline(text)

    entities = []
    for res in results:

        if res['entity_group'] == 'DISEASE_DISORDER':

            entities.append({
                "label": res['entity_group'],
                "score": float(res['score']),
                "text": res['word'],
                "start": res['start'],
                "end": res['end']
            })


    return entities


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
