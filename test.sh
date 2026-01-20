#!/bin/bash -e

curl -s -X POST http://localhost:18081/find \
  -H "Content-Type: application/json" \
  -d'{"text": "George Washington was president and he lived in Virginia. He had high blood pressure and is looking for help.", "threshold": 0.3, "labels": ["DISEASE_DISORDER"]}' | jq

# Expected output:
#[
#  {
#    "end": 84,
#    "label": "DISEASE_DISORDER",
#    "score": 0.3687628209590912,
#    "start": 64,
#    "text": "high blood pressure"
#  }
#]
