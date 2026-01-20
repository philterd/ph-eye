from flask import Flask, request
from transformers import pipeline
from waitress import serve

__version__ = "1.2.3"

app = Flask(__name__)

print("Starting ph-eye version " + __version__)
#model_name = os.environ.get("MODEL_NAME", "blaze999/Medical-NER")
print("Loading model...")
medical_ner_pipeline = pipeline("token-classification", model="/app/model/", aggregation_strategy="simple")
print("Model loaded successfully!")


@app.route("/status", methods=["GET"])
def status():
    return "healthy"


@app.route("/find", methods=["POST"])
def find():

    try:

        r = request.json

        text = r["text"]
        labels = ["DISEASE_DISORDER"] if "labels" not in r else r["labels"]
        threshold = 0.0 if "threshold" not in r else r["threshold"]

        medical_conditions = extract_medical_conditions(text)

        filtered_medical_conditions = []

        for entity in medical_conditions:
            if entity["label"] in labels and entity["score"] >= threshold:
                filtered_medical_conditions.append(entity)

        return filtered_medical_conditions, 200

    except Exception as e:
        print(str(e))
        return str(e), 500


def extract_medical_conditions(text):

    results = medical_ner_pipeline(text)

    entities = []
    for res in results:

        entities.append({
            "label": res['entity_group'],
            "score": float(res['score']),
            "text": res['word'],
            "start": res['start'] + 1,
            "end": res['end']
        })

    return entities


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
