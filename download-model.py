import os

from gliner import GLiNER

model_name = os.getenv("MODEL_NAME", "philterd/ph-eye-pii-base")
model = GLiNER.from_pretrained(model_name)
