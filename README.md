# ph-eye

ph-eye is a lightweight HTTP service that hosts AI/NLP models for finding PII and PHI in text. It exposes a simple REST
API and is designed for use with [Phileas](https://github.com/philterd/phileas)
and [Philter](https://github.com/philterd/philter), though it can also be used standalone.

- Docker images: https://hub.docker.com/repository/docker/philterd/ph-eye
- Documentation: https://philterd.github.io/ph-eye

## Available models

Each Docker image bundles a single model, selected at build time. Images are air-gapped — the model is downloaded into
the image during `docker build` and no network access is required at runtime.

| `PHEYE_MODEL`        | Language | Entities                            | Underlying model                          |
|----------------------|----------|-------------------------------------|-------------------------------------------|
| `pii_base`           | English  | General PII (person, place, org, …) | [`philterd/ph-eye-pii-base`](https://huggingface.co/philterd/ph-eye-pii-base)                |
| `hospitals`          | English  | Hospital, room number               | [`knowledgator/gliner-pii-base-v1.0`](https://huggingface.co/knowledgator/gliner-pii-base-v1.0)       |
| `medical_conditions` | English  | Disease/disorder                    | [`blaze999/Medical-NER`](https://huggingface.co/blaze999/Medical-NER)                    |
| `french_persons`     | French   | Person                              | [`EmergentMethods/gliner_medium_news-v2.1`](https://huggingface.co/EmergentMethods/gliner_medium_news-v2.1) |
| `french_medical`     | French   | Disease (`Maladie`)                 | [`almanach/camembert-bio-gliner-v0.1`](https://huggingface.co/almanach/camembert-bio-gliner-v0.1)      |

## Building

Pass `PHEYE_MODEL` as a build argument to select the model. The model is downloaded from Hugging Face and cached inside
the image at build time.

```bash
docker build --build-arg PHEYE_MODEL=pii_base            -t pheye:1.2.5-pii-base .
docker build --build-arg PHEYE_MODEL=hospitals           -t pheye:1.2.5-hospitals .
docker build --build-arg PHEYE_MODEL=medical_conditions  -t pheye:1.2.5-medical-conditions .
docker build --build-arg PHEYE_MODEL=french_persons      -t pheye:1.2.5-french-persons .
docker build --build-arg PHEYE_MODEL=french_medical      -t pheye:1.2.5-french-medical .
```

## Running

```bash
docker run -p 5000:5000 pheye:1.2.5-pii-base
```

Check that the service is up:

```bash
curl http://localhost:5000/status
```

## API

### `POST /find`

Find entities in text. `labels` and `threshold` are optional — defaults are model-specific.

**Request**

```json
{
  "text": "George Washington was president and he lived in Virginia.",
  "labels": [
    "Person",
    "Place"
  ],
  "threshold": 0.5
}
```

**Response**

```json
[
  {
    "label": "Person",
    "text": "George Washington",
    "score": 0.9923100471496582,
    "start": 0,
    "end": 17
  },
  {
    "label": "Place",
    "text": "Virginia",
    "score": 0.9528881907463074,
    "start": 48,
    "end": 56
  }
]
```

### `GET /status`

Returns `healthy` when the service is running and the model is loaded.

## License

ph-eye is licensed under the Apache License, version 2.0. The model bundled in each image may be licensed separately -
refer to the model's Hugging Face page for details.

Copyright 2024-2026 Philterd, LLC.