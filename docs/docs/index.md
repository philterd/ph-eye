# Ph-Eye

Ph-Eye is a service for hosting AI/NLP models for the purposes of finding PII and PHI in text.

Ph-Eye provides a simple REST API that accepts text and returns a list of identified entities. Each Docker image bundles
a single model selected at build time. Images are designed for air-gapped deployment — the model is baked into the image
during `docker build` and no network access is required at runtime.

Current Version: `1.3.0`

While Ph-Eye can be used standalone, it was designed and created for use
with [Phileas](https://github.com/philterd/phileas) and [Philter](https://github.com/philterd/philter) and as such
provides tight integration with each.

## Available models

| `PHEYE_MODEL`             | Language | Entities                       | Underlying model                                                                                            |
|---------------------------|----------|--------------------------------|-------------------------------------------------------------------------------------------------------------|
| `pii_en_small` (default)  | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-small`](https://huggingface.co/philterd/ph-eye-pii-en-small)                       |
| `pii_en_xsmall`           | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-xsmall`](https://huggingface.co/philterd/ph-eye-pii-en-xsmall)                     |
| `pii_en_medium`           | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-medium`](https://huggingface.co/philterd/ph-eye-pii-en-medium)                     |
| `pii_en_large`            | English  | Person names (label `name`)    | [`philterd/ph-eye-pii-en-large`](https://huggingface.co/philterd/ph-eye-pii-en-large)                       |
| `pii_base` (deprecated)   | English  | Person names (label `Person`)  | [`philterd/ph-eye-pii-base`](https://huggingface.co/philterd/ph-eye-pii-base)                               |
| `hospitals`               | English  | Hospital, room number          | [`knowledgator/gliner-pii-base-v1.0`](https://huggingface.co/knowledgator/gliner-pii-base-v1.0)             |
| `medical_conditions`      | English  | Disease/disorder               | [`blaze999/Medical-NER`](https://huggingface.co/blaze999/Medical-NER)                                       |
| `french_persons`          | French   | Person                         | [`EmergentMethods/gliner_medium_news-v2.1`](https://huggingface.co/EmergentMethods/gliner_medium_news-v2.1) |
| `french_medical`          | French   | Disease (`Maladie`)            | [`almanach/camembert-bio-gliner-v0.1`](https://huggingface.co/almanach/camembert-bio-gliner-v0.1)           |

`pii_en_small` is the default when `PHEYE_MODEL` is not set. The English name models come in four sizes (`pii_en_xsmall`, `pii_en_small`, `pii_en_medium`, `pii_en_large`) that trade speed for accuracy; each has its own recommended default threshold (0.50, 0.90, 0.70, and 0.95 respectively). `pii_base` is deprecated and remains available only when explicitly selected.

## Features

- **Multiple models**: Choose the model best suited to your use case at build time.
- **Air-gapped deployment**: Models are downloaded at image build time — no outbound network access needed at runtime.
- **GPU support**: GPU-enabled images are available via `Dockerfile.gpu` for accelerated inference with CUDA 12.1.
- **REST API**: Simple JSON-based API for easy integration.
- **Dockerized**: Easily deployable as a Docker container.
- **Integration**: Works seamlessly with Phileas and Philter.

## License

Ph-Eye is licensed under the Apache License, version 2.0. The model bundled in each image may be licensed separately -
refer to the model's Hugging Face page for details.

Copyright 2026 Philterd, LLC.