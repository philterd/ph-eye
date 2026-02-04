from flask import Flask, request
from gliner import GLiNER
from waitress import serve

__version__ = "1.2.3"

app = Flask(__name__)

print("Starting ph-eye version " + __version__)
print("Loading model...")
model = GLiNER.from_pretrained("almanach/camembert-bio-gliner-v0.1")
print("Model loaded successfully!")


@app.route("/status", methods=["GET"])
def status():
    return "healthy"


@app.route("/find", methods=["POST"])
def find():

    try:

        r = request.json

        text = r["text"]
        labels = ["Maladie"] if "labels" not in r else r["labels"]
        threshold = 0.3 if "threshold" not in r else r["threshold"]

        entities = model.predict_entities(text, labels, threshold=threshold, flat_ner=True)

        returned_entities = []
        for res in entities:

            returned_entities.append({
                "label": res['label'],
                "score": float(res['score']),
                "text": res['text'],
                "start": res['start'],
                "end": res['end']
            })

        return returned_entities, 200


    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
