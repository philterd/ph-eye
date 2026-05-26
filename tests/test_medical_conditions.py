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

import models.medical_conditions as module

DISEASE_RESULT = {"entity_group": "DISEASE_DISORDER", "score": 0.92, "word": "diabetes", "start": 14, "end": 22}
OTHER_RESULT = {"entity_group": "OTHER", "score": 0.88, "word": "insulin", "start": 26, "end": 33}
LOW_SCORE_RESULT = {"entity_group": "DISEASE_DISORDER", "score": 0.1, "word": "flu", "start": 5, "end": 8}


def test_default_labels_is_nonempty_list():
    assert isinstance(module.DEFAULT_LABELS, list)
    assert len(module.DEFAULT_LABELS) > 0


def test_default_threshold_is_float_in_range():
    assert isinstance(module.DEFAULT_THRESHOLD, float)
    assert 0.0 <= module.DEFAULT_THRESHOLD <= 1.0


def test_predict_returns_entity():
    pipeline = MagicMock()
    pipeline.return_value = [DISEASE_RESULT]
    result = module.predict(pipeline, "Patient has diabetes.", ["DISEASE_DISORDER"], 0.0)
    assert len(result) == 1
    assert result[0]["label"] == "DISEASE_DISORDER"
    assert result[0]["text"] == "diabetes"
    assert result[0]["end"] == 22


def test_predict_applies_start_offset():
    pipeline = MagicMock()
    pipeline.return_value = [DISEASE_RESULT]
    result = module.predict(pipeline, "text", ["DISEASE_DISORDER"], 0.0)
    assert result[0]["start"] == DISEASE_RESULT["start"] + 1


def test_predict_score_is_float():
    pipeline = MagicMock()
    pipeline.return_value = [DISEASE_RESULT]
    result = module.predict(pipeline, "text", ["DISEASE_DISORDER"], 0.0)
    assert isinstance(result[0]["score"], float)


def test_predict_filters_by_label():
    pipeline = MagicMock()
    pipeline.return_value = [DISEASE_RESULT, OTHER_RESULT]
    result = module.predict(pipeline, "text", ["DISEASE_DISORDER"], 0.0)
    assert len(result) == 1
    assert result[0]["label"] == "DISEASE_DISORDER"


def test_predict_filters_by_threshold():
    pipeline = MagicMock()
    pipeline.return_value = [DISEASE_RESULT, LOW_SCORE_RESULT]
    result = module.predict(pipeline, "text", ["DISEASE_DISORDER"], 0.5)
    assert len(result) == 1
    assert result[0]["text"] == "diabetes"


def test_predict_filters_by_label_and_threshold():
    pipeline = MagicMock()
    pipeline.return_value = [DISEASE_RESULT, OTHER_RESULT, LOW_SCORE_RESULT]
    result = module.predict(pipeline, "text", ["DISEASE_DISORDER"], 0.5)
    assert len(result) == 1
    assert result[0]["label"] == "DISEASE_DISORDER"
    assert result[0]["text"] == "diabetes"


def test_predict_returns_empty_list_when_no_entities():
    pipeline = MagicMock()
    pipeline.return_value = []
    result = module.predict(pipeline, "text", ["DISEASE_DISORDER"], 0.0)
    assert result == []
