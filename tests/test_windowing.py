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


import re
from types import SimpleNamespace
from unittest.mock import MagicMock

import windowing

NAME = re.compile(r"Name\d+(?: Name\d+)?")


def truncating_predictor(max_words, calls):
    """A model that, like GLiNER, reads only its first max_words words, and reports the names among them."""
    def predict_window(text):
        calls.append(text)
        end = 0
        for i, word in enumerate(windowing.WORD.finditer(text)):
            if i == max_words:
                break
            end = word.end()
        return [{"label": "name", "score": 0.9, "text": m.group(), "start": m.start(), "end": m.end()}
                for m in NAME.finditer(text[:end])]
    return predict_window


def names_everywhere(count):
    """Two-word names at every offset, so some cross every seam between windows."""
    parts, n = [], 0
    for i in range(count):
        parts.append(f"Name{n} Name{n + 1}" + " and" * (i % 3) + ", ")
        n += 2
    return "".join(parts)


def text_of(words):
    return " ".join(f"w{i}" for i in range(words))


def test_text_that_fits_is_one_window_passed_as_it_is():
    calls = []
    text = "  Name1 Name2 met the clerk.  "
    entities = windowing.predict(text, truncating_predictor(50, calls), 50, 12)
    assert calls == [text]
    assert [(e["start"], e["end"]) for e in entities] == [(2, 13)]


def test_one_word_over_the_limit_is_two_windows():
    assert len(windowing.windows(text_of(51), 50, 12)) == 2


def test_punctuation_counts_as_a_word():
    assert len(windowing.WORD.findall("a,b,c,d,e,f")) == 11
    assert len(windowing.WORD.findall("well-known snake_case Zoë")) == 3


def test_overlap_is_at_least_twice_the_width_and_at_most_half_a_window():
    assert windowing.overlap(512, 12) == 64
    assert windowing.overlap(512, 50) == 100
    assert windowing.overlap(50, 12) == 25


def test_every_entity_is_owned_by_exactly_one_window_that_contains_it():
    for max_words, max_width in [(512, 12), (256, 12), (50, 3), (10, 2), (7, 3)]:
        for count in [max_words + 1, 2 * max_words, 5 * max_words + 3, 1000]:
            text = text_of(count) + ", and; more."
            words = [(m.start(), m.end()) for m in windowing.WORD.finditer(text)]
            spans = windowing.windows(text, max_words, max_width)
            assert spans[0][2] == 0 and spans[-1][3] == len(text)
            for i, (start, end, owned_start, owned_end) in enumerate(spans):
                assert len(windowing.WORD.findall(text[start:end])) <= max_words
                if i:
                    assert spans[i - 1][3] == owned_start
            for first in range(len(words)):
                start = words[first][0]
                end = words[min(first + max_width, len(words)) - 1][1]
                owners = [w for w in spans if w[2] <= start < w[3]]
                assert len(owners) == 1
                if 2 * max_width <= windowing.overlap(max_words, max_width):
                    assert owners[0][0] <= start and end <= owners[0][1]


def test_every_name_is_found_once_and_whole():
    calls = []
    text = names_everywhere(120)
    entities = windowing.predict(text, truncating_predictor(50, calls), 50, 2)

    assert sorted((e["start"], e["end"]) for e in entities) == [(m.start(), m.end()) for m in NAME.finditer(text)]
    assert all(text[e["start"]:e["end"]] == e["text"] for e in entities)
    assert len(calls) > 5


def test_without_windowing_names_after_the_limit_are_missed():
    # The behavior windowing corrects: one call sees only the first max_words words.
    text = names_everywhere(120)
    assert len(truncating_predictor(50, [])(text)) < len(NAME.findall(text))


def test_limits_come_from_the_module_then_the_model_configuration():
    gliner = SimpleNamespace(config=SimpleNamespace(max_len=384, max_width=10))
    assert windowing.limits(SimpleNamespace(), gliner) == (384, 10)
    assert windowing.limits(SimpleNamespace(MAX_WORDS=200), gliner) == (200, 10)
    assert windowing.limits(SimpleNamespace(), object()) == (windowing.DEFAULT_MAX_WORDS, windowing.DEFAULT_MAX_WIDTH)


def test_limits_ignore_values_that_are_not_positive_integers():
    assert windowing.limits(MagicMock(), MagicMock()) == (windowing.DEFAULT_MAX_WORDS, windowing.DEFAULT_MAX_WIDTH)
    bad = SimpleNamespace(config=SimpleNamespace(max_len=0, max_width=True))
    assert windowing.limits(SimpleNamespace(MAX_WORDS="512"), bad) == (
        windowing.DEFAULT_MAX_WORDS, windowing.DEFAULT_MAX_WIDTH)
