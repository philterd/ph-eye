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

from unittest.mock import MagicMock

import models.hospitals as module

HOSPITAL_ENTITY = {"label": "hospital", "score": 0.9, "text": "St. Mary's", "start": 10, "end": 20}
ROOM_ENTITY = {"label": "room number", "score": 0.3, "text": "Room 5", "start": 25, "end": 31}


def test_default_labels_is_nonempty_list():
    assert isinstance(module.DEFAULT_LABELS, list)
    assert len(module.DEFAULT_LABELS) > 0


def test_default_threshold_is_float_in_range():
    assert isinstance(module.DEFAULT_THRESHOLD, float)
    assert 0.0 <= module.DEFAULT_THRESHOLD <= 1.0


def test_predict_returns_entity():
    model = MagicMock()
    model.predict_entities.return_value = [HOSPITAL_ENTITY]
    result = module.predict(model, "text", ["hospital"], 0.0)
    assert len(result) == 1
    assert result[0]["label"] == "hospital"
    assert result[0]["text"] == "St. Mary's"
    assert result[0]["start"] == 10
    assert result[0]["end"] == 20


def test_predict_score_is_float():
    model = MagicMock()
    model.predict_entities.return_value = [HOSPITAL_ENTITY]
    result = module.predict(model, "text", ["hospital"], 0.0)
    assert isinstance(result[0]["score"], float)


def test_predict_does_not_pass_threshold_to_model():
    model = MagicMock()
    model.predict_entities.return_value = []
    module.predict(model, "text", ["hospital"], 0.5)
    model.predict_entities.assert_called_once_with("text", ["hospital"])


def test_predict_filters_by_threshold():
    model = MagicMock()
    model.predict_entities.return_value = [HOSPITAL_ENTITY, ROOM_ENTITY]
    result = module.predict(model, "text", ["hospital", "room number"], 0.5)
    assert len(result) == 1
    assert result[0]["label"] == "hospital"


def test_predict_returns_empty_list_when_no_entities():
    model = MagicMock()
    model.predict_entities.return_value = []
    result = module.predict(model, "text", ["hospital"], 0.5)
    assert result == []


def test_predict_returns_empty_list_when_all_below_threshold():
    model = MagicMock()
    model.predict_entities.return_value = [ROOM_ENTITY]
    result = module.predict(model, "text", ["room number"], 0.5)
    assert result == []
