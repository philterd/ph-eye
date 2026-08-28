# ph-eye

ph-eye is a lightweight HTTP service that hosts AI/NLP models for finding PII and PHI in text. It exposes a simple REST
API and is designed for use with [Phileas](https://github.com/philterd/phileas)
and [Philter](https://github.com/philterd/philter), though it can also be used standalone.

- Docker images: https://hub.docker.com/repository/docker/philterd/ph-eye
- Documentation: https://philterd.github.io/ph-eye

## Available models

Each Docker image bundles a single model, selected at build time. Images are air-gapped — the model is downloaded into
the image during `docker build` and no network access is required at runtime.

| `PHEYE_MODEL`             | Language | Entities                       | Underlying model                          |
|---------------------------|----------|--------------------------------|-------------------------------------------|
| `pii_en_small` (default)  | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-small`](https://huggingface.co/philterd/ph-eye-pii-en-small)        |
| `pii_en_xsmall`           | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-xsmall`](https://huggingface.co/philterd/ph-eye-pii-en-xsmall)      |
| `pii_en_medium`           | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-medium`](https://huggingface.co/philterd/ph-eye-pii-en-medium)      |
| `pii_en_large`            | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-large`](https://huggingface.co/philterd/ph-eye-pii-en-large)        |
| `pii_base` (deprecated)   | English  | Person names (label `Person`)  | [`philterd/ph-eye-pii-base`](https://huggingface.co/philterd/ph-eye-pii-base)                |
| `hospitals`               | English  | Hospital, room number          | [`knowledgator/gliner-pii-base-v1.0`](https://huggingface.co/knowledgator/gliner-pii-base-v1.0)       |
| `medical_conditions`      | English  | Disease/disorder               | [`blaze999/Medical-NER`](https://huggingface.co/blaze999/Medical-NER)                    |
| `french_persons`          | French   | Person                         | [`EmergentMethods/gliner_medium_news-v2.1`](https://huggingface.co/EmergentMethods/gliner_medium_news-v2.1) |
| `french_medical`          | French   | Disease (`Maladie`)            | [`almanach/camembert-bio-gliner-v0.1`](https://huggingface.co/almanach/camembert-bio-gliner-v0.1)      |

`pii_en_small` is the default when `PHEYE_MODEL` is not set. The English name models come in four sizes (`pii_en_xsmall`, `pii_en_small`, `pii_en_medium`, `pii_en_large`) that trade speed for accuracy; each has its own recommended default threshold (0.50, 0.90, 0.70, and 0.95 respectively). `pii_base` is deprecated and remains available only when explicitly selected.

## Building

Pass `PHEYE_MODEL` as a build argument to select the model. The model is downloaded from Hugging Face and cached inside
the image at build time.

```bash
docker build --build-arg PHEYE_MODEL=pii_en_small        -t pheye:1.3.0-pii-en-small .
docker build --build-arg PHEYE_MODEL=pii_en_xsmall       -t pheye:1.3.0-pii-en-xsmall .
docker build --build-arg PHEYE_MODEL=pii_en_medium       -t pheye:1.3.0-pii-en-medium .
docker build --build-arg PHEYE_MODEL=pii_en_large        -t pheye:1.3.0-pii-en-large .
docker build --build-arg PHEYE_MODEL=pii_base            -t pheye:1.3.0-pii-base .
docker build --build-arg PHEYE_MODEL=hospitals           -t pheye:1.3.0-hospitals .
docker build --build-arg PHEYE_MODEL=medical_conditions  -t pheye:1.3.0-medical-conditions .
docker build --build-arg PHEYE_MODEL=french_persons      -t pheye:1.3.0-french-persons .
docker build --build-arg PHEYE_MODEL=french_medical      -t pheye:1.3.0-french-medical .
```

## Running

```bash
docker run -p 5000:5000 pheye:1.3.0-pii-en-small
```

To run all models together using Docker Compose:

```bash
docker compose up                        # CPU
docker compose -f docker-compose.gpu.yaml up   # GPU
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
  "text": "Please forward the invoice to Toni Levine and copy Maria Gonzalez.",
  "labels": [
    "name"
  ],
  "threshold": 0.9
}
```

The default `pii_en_small` model uses the label `name` and a threshold of `0.9`. Omit `labels` and `threshold` to use the model defaults.

**Response**

```json
[
  {
    "label": "name",
    "text": "Toni Levine",
    "score": 0.9712,
    "start": 30,
    "end": 41
  },
  {
    "label": "name",
    "text": "Maria Gonzalez",
    "score": 0.9685,
    "start": 51,
    "end": 65
  }
]
```

### `GET /status`

Returns a standard JSON health response when the service is running and the model is loaded.

```json
{
  "status": "UP",
  "applicationVersion": "1.3.0"
}
```

## License

ph-eye is licensed under the Apache License, version 2.0. The model bundled in each image may be licensed separately -
refer to the model's Hugging Face page for details.

Copyright 2024-2026 Philterd, LLC.
