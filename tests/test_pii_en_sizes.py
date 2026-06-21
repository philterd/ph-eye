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

# Interface tests for the English name model size variants (xsmall, medium,
# large). pii_en_small has its own dedicated test module.

import importlib
from unittest.mock import MagicMock

import pytest

MODULES = ["pii_en_xsmall", "pii_en_medium", "pii_en_large"]


@pytest.fixture(params=MODULES)
def module(request):
    return importlib.import_module(f"models.{request.param}")


def test_default_label_is_name(module):
    assert module.DEFAULT_LABELS == ["name"]


def test_default_threshold_is_float_in_range(module):
    assert isinstance(module.DEFAULT_THRESHOLD, float)
    assert 0.0 <= module.DEFAULT_THRESHOLD <= 1.0


def test_revision_is_pinned(module):
    # Air-gapped, reproducible builds require a pinned Hugging Face revision.
    assert isinstance(module.DEFAULT_REVISION, str)
    assert len(module.DEFAULT_REVISION) == 40  # full git commit sha


def test_predict_returns_entity(module):
    model = MagicMock()
    model.predict_entities.return_value = [
        {"label": "name", "score": 0.97, "text": "George Washington", "start": 0, "end": 17}
    ]
    result = module.predict(model, "George Washington was president.", ["name"], module.DEFAULT_THRESHOLD)
    assert len(result) == 1
    assert result[0]["label"] == "name"
    assert result[0]["text"] == "George Washington"
    assert isinstance(result[0]["score"], float)


def test_predict_passes_threshold_to_model(module):
    model = MagicMock()
    model.predict_entities.return_value = []
    module.predict(model, "text", ["name"], 0.8)
    model.predict_entities.assert_called_once_with("text", ["name"], threshold=0.8)
