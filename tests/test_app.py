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

import os
import sys
from unittest.mock import MagicMock

import pytest

# Install a mock model module under a unique key before app.py is imported.
# app.py runs importlib.import_module("models.<PHEYE_MODEL>") at module level,
# so the mock must be in sys.modules before the import happens.
_mock_model = MagicMock()

_mock_module = MagicMock()
_mock_module.DEFAULT_LABELS = ["Person"]
_mock_module.DEFAULT_THRESHOLD = 0.5
_mock_module.load.return_value = _mock_model
_mock_module.predict.return_value = [
    {"label": "Person", "score": 0.9, "text": "John Smith", "start": 0, "end": 10}
]

sys.modules["models._mock"] = _mock_module
os.environ["PHEYE_MODEL"] = "_mock"

import app as flask_app  # noqa: E402 — must come after sys.modules setup


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def reset_mock():
    _mock_module.predict.return_value = [
        {"label": "Person", "score": 0.9, "text": "John Smith", "start": 0, "end": 10}
    ]
    _mock_module.DEFAULT_LABELS = ["Person"]
    _mock_module.DEFAULT_THRESHOLD = 0.5
    yield


# --- /status ---

def test_status_returns_standard_health_response(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "UP", "applicationVersion": "1.3.0"}


# --- /find ---

def test_find_returns_200(client):
    response = client.post("/find", json={"text": "John Smith went home."})
    assert response.status_code == 200


def test_find_returns_entities(client):
    response = client.post("/find", json={"text": "John Smith went home."})
    entities = response.get_json()
    assert len(entities) == 1
    assert entities[0]["label"] == "Person"
    assert entities[0]["text"] == "John Smith"


def test_find_uses_provided_labels(client):
    client.post("/find", json={"text": "some text.", "labels": ["Place"]})
    _, kwargs = _mock_module.predict.call_args
    args = _mock_module.predict.call_args[0]
    assert args[2] == ["Place"]


def test_find_uses_default_labels_when_omitted(client):
    client.post("/find", json={"text": "some text."})
    args = _mock_module.predict.call_args[0]
    assert args[2] == _mock_module.DEFAULT_LABELS


def test_find_uses_default_labels_when_empty(client):
    client.post("/find", json={"text": "some text.", "labels": []})
    args = _mock_module.predict.call_args[0]
    assert args[2] == _mock_module.DEFAULT_LABELS


def test_find_uses_provided_threshold(client):
    client.post("/find", json={"text": "some text.", "threshold": 0.8})
    args = _mock_module.predict.call_args[0]
    assert args[3] == 0.8


def test_find_uses_default_threshold_when_omitted(client):
    client.post("/find", json={"text": "some text."})
    args = _mock_module.predict.call_args[0]
    assert args[3] == _mock_module.DEFAULT_THRESHOLD


def test_find_passes_text_to_predict(client):
    client.post("/find", json={"text": "John Smith went home."})
    args = _mock_module.predict.call_args[0]
    assert args[1] == "John Smith went home."


def test_find_returns_500_on_exception(client):
    _mock_module.predict.side_effect = Exception("model failure")
    response = client.post("/find", json={"text": "some text."})
    assert response.status_code == 500
    _mock_module.predict.side_effect = None
