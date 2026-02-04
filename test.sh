#!/bin/bash -e

curl -s -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d'{"text": "Je m''appelle Mary et je suis diabétique.", "threshold": 0.3, "labels": ["Maladie"]}' | jq

# Expected output:
#[
#  {
#    "end": 38,
#    "label": "Maladie",
#    "score": 0.7531318068504333,
#    "start": 29,
#    "text": "diabétique"
#  }
#]