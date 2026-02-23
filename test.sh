#!/bin/bash -e

curl -s -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d'{"text": "He was in Buffalo Hospital and then ECMC Hospital.", "threshold": 0.3}' | jq

# Expected output:
#[
#  {
#    "end": 26,
#    "label": "hospital",
#    "score": 0.9917145371437073,
#    "start": 11,
#    "text": "Buffalo Hospital"
#  },
#  {
#    "end": 49,
#    "label": "hospital",
#    "score": 0.9758248329162598,
#    "start": 37,
#    "text": "ECMC Hospital"
#  }
#]
