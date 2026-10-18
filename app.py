# Copyright 2024-2026 Philterd, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
import os

from flask import Flask, jsonify, request
from waitress import serve

import device
import windowing

__version__ = "1.4.0"

app = Flask(__name__)

model_id = os.environ.get("PHEYE_MODEL", "pii_en_small")
print(f"Starting ph-eye version {__version__} with model '{model_id}'")

model_module = importlib.import_module(f"models.{model_id}")
model, model_device = device.place(model_module.load())
max_words, max_width = windowing.limits(model_module, model)
print(f"Model loaded on {model_device} and ready to serve requests; it examines up to {max_words} words per call")


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="UP", applicationVersion=__version__)


@app.route("/model", methods=["GET"])
def model_info():
    # What a client needs to send text the model reads whole: the most words it examines in one call
    # and the most words one entity covers.
    return jsonify(name=model_id, maxWords=max_words, maxWidth=max_width)


@app.route("/find", methods=["POST"])
def find():
    try:
        r = request.json
        text = r["text"]
        labels = r.get("labels") or model_module.DEFAULT_LABELS
        threshold = r["threshold"] if "threshold" in r else model_module.DEFAULT_THRESHOLD

        entities = windowing.predict(
            text, lambda window: model_module.predict(model, window, labels, threshold), max_words, max_width)
        return entities, 200

    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
