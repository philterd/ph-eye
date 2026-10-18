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

# Puts the loaded model on the GPU when one is available. GLiNER loads to the CPU
# (GLiNER.from_pretrained defaults to map_location="cpu") and stays there unless moved, so a -gpu
# image would otherwise run on the CPU. A transformers pipeline chooses its own device.


def place(model):
    """Moves a PyTorch model to CUDA when it is available. Returns the model and its device's name."""
    try:
        import torch
    except ImportError:
        return model, "cpu"

    if isinstance(model, torch.nn.Module):
        if torch.cuda.is_available():
            model = model.to("cuda")
        return model, str(next(model.parameters(), torch.empty(0)).device)

    device = getattr(model, "device", None)
    return model, str(device) if device is not None else "cpu"
