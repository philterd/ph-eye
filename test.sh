#!/bin/bash -e

curl -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d'{"text": "George Washington was president and he lived in Virginia.", "threshold": 0.50, "labels": ["Person", "Place"]}'
  