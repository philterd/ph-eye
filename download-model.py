import os

from transformers import pipeline

model_name = os.environ.get("MODEL_NAME", "blaze999/Medical-NER")
print("Downloading model...")
medical_ner_pipeline = pipeline("token-classification", model=model_name, aggregation_strategy="simple")
print("Model downloaded.")
