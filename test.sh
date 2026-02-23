#!/bin/bash -e

curl -s -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d'{"text": "He was in Buffalo Hospital in 1008 and then ECMC Hospital. He was in room 303.", "threshold": 0.3}' | jq

# Expected output:
#[
#  {
#    "end": 26,
#    "label": "hospital",
#    "score": 0.9859573841094971,
#    "start": 11,
#    "text": "Buffalo Hospital"
#  },
#  {
#    "end": 34,
#    "label": "room number",
#    "score": 0.7561585903167725,
#    "start": 31,
#    "text": "1008"
#  },
#  {
#    "end": 57,
#    "label": "hospital",
#    "score": 0.9503083825111389,
#    "start": 45,
#    "text": "ECMC Hospital"
#  },
#  {
#    "end": 77,
#    "label": "room number",
#    "score": 0.6244677305221558,
#    "start": 75,
#    "text": "303"
#  }
#]
