#!/bin/bash -e

curl -s -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d'{"text": "Bonjour, je m''appelle Sophie.", "threshold": 0.3, "labels": ["person"]}' | jq

# Expected output:
#[
#  {
#    "end": 27,
#    "label": "person",
#    "score": 0.9863523244857788,
#    "start": 22,
#    "text": "Sophie"
#  }
#]