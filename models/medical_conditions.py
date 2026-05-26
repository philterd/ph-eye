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

DEFAULT_LABELS = ["DISEASE_DISORDER"]
DEFAULT_THRESHOLD = 0.0


def load():
    from transformers import pipeline
    print("Loading model blaze999/Medical-NER...")
    model = pipeline("token-classification", model="blaze999/Medical-NER", aggregation_strategy="simple")
    print("Model loaded successfully!")
    return model


def predict(model, text, labels, threshold):
    results = model(text)
    return [
        {
            "label": res["entity_group"],
            "score": float(res["score"]),
            "text": res["word"],
            "start": res["start"] + 1,
            "end": res["end"],
        }
        for res in results
        if res["entity_group"] in labels and float(res["score"]) >= threshold
    ]
