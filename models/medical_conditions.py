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

# Not a GLiNER model, so its configuration gives no word limit. Its detections fall off as text grows
# (from three of three conditions at 296 words to none at 4,216), so /find sends it windows of this
# many words. 200 and 256 kept the same conditions in testing; 128 lost one at 296 words.
MAX_WORDS = 256


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
