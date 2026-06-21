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

# Default English PII model. Detects person names using the single label "name"
# at a recommended threshold of 0.90. Supersedes the deprecated "pii_base" model.

import os

DEFAULT_LABELS = ["name"]
DEFAULT_THRESHOLD = 0.9

DEFAULT_MODEL = "philterd/ph-eye-pii-en-small"
# Pin a specific Hugging Face revision so Docker builds are reproducible and the
# air-gapped runtime always bundles the same weights.
DEFAULT_REVISION = "375cfd7bd6b4fa0ef618333048b9e94b92c35c94"


def load():
    from gliner import GLiNER
    model_name = os.getenv("MODEL_NAME", DEFAULT_MODEL)
    # Pin the revision for the bundled default model. If MODEL_NAME is overridden,
    # honor MODEL_REVISION when set, otherwise let the hub resolve the main branch.
    revision = os.getenv("MODEL_REVISION") or (
        DEFAULT_REVISION if model_name == DEFAULT_MODEL else None
    )
    print(f"Loading model {model_name} (revision {revision or 'main'})...")
    model = GLiNER.from_pretrained(model_name, revision=revision)
    print("Model loaded successfully!")
    return model


def predict(model, text, labels, threshold):
    entities = model.predict_entities(text, labels, threshold=threshold)
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
