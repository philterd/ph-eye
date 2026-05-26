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

from gliner import GLiNER

DEFAULT_LABELS = ["Maladie"]
DEFAULT_THRESHOLD = 0.3


def load():
    print("Loading model almanach/camembert-bio-gliner-v0.1...")
    model = GLiNER.from_pretrained("almanach/camembert-bio-gliner-v0.1")
    print("Model loaded successfully!")
    return model


def predict(model, text, labels, threshold):
    entities = model.predict_entities(text, labels, threshold=threshold, flat_ner=True)
    return [
        {
            "label": e["label"],
            "score": float(e["score"]),
            "text": e["text"],
            "start": e["start"],
            "end": e["end"],
        }
        for e in entities
    ]
