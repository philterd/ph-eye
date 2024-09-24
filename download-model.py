import os

from gliner import GLiNER

model_name = os.getenv("MODEL_NAME", "urchade/gliner_mediumv2.1")
model = GLiNER.from_pretrained(model_name)
