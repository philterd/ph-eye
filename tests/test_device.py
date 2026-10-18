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


import sys
from types import SimpleNamespace

import pytest

import device


class FakeModule:
    """Stands in for torch.nn.Module: records where it was moved."""

    def __init__(self):
        self.where = "cpu"

    def to(self, where):
        self.where = where
        return self

    def parameters(self):
        return iter([SimpleNamespace(device=self.where)])


@pytest.fixture
def fake_torch(monkeypatch):
    def install(cuda):
        torch = SimpleNamespace(nn=SimpleNamespace(Module=FakeModule),
                                cuda=SimpleNamespace(is_available=lambda: cuda),
                                empty=lambda n: SimpleNamespace(device="cpu"))
        monkeypatch.setitem(sys.modules, "torch", torch)
    return install


def test_a_pytorch_model_is_moved_to_cuda_when_it_is_available(fake_torch):
    fake_torch(cuda=True)
    model, where = device.place(FakeModule())
    assert model.where == "cuda"
    assert where == "cuda"


def test_a_pytorch_model_stays_on_the_cpu_without_cuda(fake_torch):
    fake_torch(cuda=False)
    model, where = device.place(FakeModule())
    assert model.where == "cpu"
    assert where == "cpu"


def test_a_pipeline_is_left_where_it_placed_itself(fake_torch):
    fake_torch(cuda=True)
    pipeline = SimpleNamespace(device="cuda:0")
    model, where = device.place(pipeline)
    assert model is pipeline
    assert where == "cuda:0"


def test_without_torch_the_model_is_left_alone(monkeypatch):
    monkeypatch.setitem(sys.modules, "torch", None)
    model = object()
    assert device.place(model) == (model, "cpu")
