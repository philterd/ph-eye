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

__version__ = "1.3.0"

app = Flask(__name__)

model_id = os.environ.get("PHEYE_MODEL", "pii_en_small")
print(f"Starting ph-eye version {__version__} with model '{model_id}'")

model_module = importlib.import_module(f"models.{model_id}")
model = model_module.load()
print("Model loaded and ready to serve requests")


@app.route("/status", methods=["GET"])
def status():
    return jsonify(status="UP", applicationVersion=__version__)


@app.route("/find", methods=["POST"])
def find():
    try:
        r = request.json
        text = r["text"]
        labels = r.get("labels") or model_module.DEFAULT_LABELS
        threshold = r["threshold"] if "threshold" in r else model_module.DEFAULT_THRESHOLD

        entities = model_module.predict(model, text, labels, threshold)
        return entities, 200

    except Exception as e:
        print(str(e))
        return str(e), 500


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
