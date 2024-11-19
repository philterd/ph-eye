# ph-eye

ph-eye is a service for hosting AI/NLP models for the purposes of finding PII and PHI in text. PH-Eye can be used standalone but it was designed and created for use with [Phileas](https://github.com/philterd/phileas) and [Philter](https://github.com/philterd/philter) and as such provides tight integration with each.

Docker images are available at https://hub.docker.com/repository/docker/philterd/ph-eye.

Text can be sent to the service as:

```
curl -X POST http://localhost:5000/find \
  -H "Content-Type: application/json" \
  -d'{
  "text": "George Washington was president and he lived in Virginia.",
  "threshold": 0.5,
  "labels": [
    "Person",
    "Place"
  ]
}'
```

With the response:

```
[
  {
    "end": 17,
    "label": "Person",
    "score": 0.9923100471496582,
    "start": 0,
    "text": "George Washington"
  },
  {
    "end": 56,
    "label": "Place",
    "score": 0.9528881907463074,
    "start": 48,
    "text": "Virginia"
  }
]
```

## License

ph-eye is licensed under the Apache License, version 2.0. However, the model(s) used by ph-eye may be used under a different license. Please refer to the specific model being used for information about its license.
