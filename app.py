from flask import Flask, request
from gliner import GLiNER
from waitress import serve

__version__ = "1.2.3"

app = Flask(__name__)

print("Starting ph-eye version " + __version__)
print("Loading model...")
model = GLiNER.from_pretrained("knowledgator/gliner-pii-base-v1.0")
print("Model loaded successfully!")


@app.route("/status", methods=["GET"])
def status():
    return "healthy"


@app.route("/find", methods=["POST"])
def find():

    try:

        r = request.json

        text = r["text"]
        labels = ["hospital", "room number"] if "labels" not in r else r["labels"]
        threshold = 0.0 if "threshold" not in r else r["threshold"]

        entities = model.predict_entities(text, labels)

        returned_entities = []

        for entity in entities:
            #print(entity["text"], "=>", entity["label"])
            returned_entities.append({
                "label": entity['label'],
                "score": float(entity['score']),
                "text": entity['text'],
                "start": entity['start'],
                "end": entity['end']
            })

        return returned_entities, 200

    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
