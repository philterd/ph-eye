# Copyright 2026 Philterd, LLC
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

# Detects over text longer than a model examines in one call. A GLiNER model reads at most max_len
# words and ignores the rest, so /find divides longer text into overlapping windows that each fit.
#
# Words are counted as GLiNER's whitespace splitter counts them, so a punctuation mark is a word.
# Each window owns the words between the midpoints of its overlaps with its neighbors, and an entity
# is kept only from the window that owns its first word. With half the overlap at least the longest
# entity a model reports (max_width), a kept entity lies wholly inside its window, and no entity is
# reported twice. The same scheme is used by Phileas's PhEye filter.

import re

# GLiNER's whitespace word splitter. Python's \w is Unicode by default, as GLiNER's is.
WORD = re.compile(r"\w+(?:[-_]\w+)*|\S")

# The fewest words two windows share, for context on both sides of an entity near their seam.
MIN_OVERLAP = 64

# Limits for a model that declares none and whose configuration does not give them.
DEFAULT_MAX_WORDS = 256
DEFAULT_MAX_WIDTH = 12


def _positive_int(value):
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else None


def limits(module, model):
    """The most words the model examines in one call, and the most words one entity covers.

    A model module may set MAX_WORDS and MAX_WIDTH. Otherwise a GLiNER model's max_len and max_width
    are read from its configuration, and anything else gets the defaults.
    """
    config = getattr(model, "config", None)
    max_words = (_positive_int(getattr(module, "MAX_WORDS", None))
                 or _positive_int(getattr(config, "max_len", None))
                 or DEFAULT_MAX_WORDS)
    max_width = (_positive_int(getattr(module, "MAX_WIDTH", None))
                 or _positive_int(getattr(config, "max_width", None))
                 or DEFAULT_MAX_WIDTH)
    return max_words, max_width


def overlap(max_words, max_width):
    """At least MIN_OVERLAP and twice max_width, and at most half a window, so each window advances."""
    return min(max(MIN_OVERLAP, 2 * max_width), max_words // 2)


def windows(text, max_words, max_width):
    """The windows of a text as (start, end, owned_start, owned_end) character offsets.

    [start, end) is the text the model sees and [owned_start, owned_end) the part whose entities the
    window reports. Text of at most max_words words is one window covering all of it.
    """
    words = [(m.start(), m.end()) for m in WORD.finditer(text)]
    count = len(words)
    if max_words < 1 or count <= max_words:
        return [(0, len(text), 0, len(text))]

    half = overlap(max_words, max_width) // 2
    step = max_words - 2 * half

    result = []
    first = 0
    while True:
        first_window = first == 0
        last_window = first + max_words >= count
        start = 0 if first_window else words[first][0]
        end = len(text) if last_window else words[first + max_words - 1][1]
        owned_start = 0 if first_window else words[first + half][0]
        owned_end = len(text) if last_window else words[first + max_words - half][0]
        result.append((start, end, owned_start, owned_end))
        if last_window:
            return result
        first += step


def predict(text, predict_window, max_words, max_width):
    """Runs predict_window over each window of the text and returns its entities with offsets into the text.

    predict_window takes a string and returns entity dicts with "start" and "end" offsets into it.
    Text that fits is passed to it as it is.
    """
    spans = windows(text, max_words, max_width)
    if len(spans) == 1:
        return predict_window(text)

    entities = []
    for start, end, owned_start, owned_end in spans:
        for entity in predict_window(text[start:end]):
            entity_start = entity["start"] + start
            if owned_start <= entity_start < owned_end:
                entities.append(dict(entity, start=entity_start, end=entity["end"] + start))
    return entities
