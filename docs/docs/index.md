# Ph-Eye

Ph-Eye is a service for hosting AI/NLP models for the purposes of finding PII and PHI in text.

Ph-Eye provides a simple REST API that accepts text and returns a list of identified entities. Each Docker image bundles
a single model selected at build time. Images are designed for air-gapped deployment — the model is baked into the image
during `docker build` and no network access is required at runtime.

Current Version: `1.2.5`

While Ph-Eye can be used standalone, it was designed and created for use
with [Phileas](https://github.com/philterd/phileas) and [Philter](https://github.com/philterd/philter) and as such
provides tight integration with each.

## Available models

| `PHEYE_MODEL`        | Language | Entities                            | Underlying model                                                                                            |
|----------------------|----------|-------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `pii_base`           | English  | General PII (person, place, org, …) | [`philterd/ph-eye-pii-base`](https://huggingface.co/philterd/ph-eye-pii-base)                               |
| `hospitals`          | English  | Hospital, room number               | [`knowledgator/gliner-pii-base-v1.0`](https://huggingface.co/knowledgator/gliner-pii-base-v1.0)             |
| `medical_conditions` | English  | Disease/disorder                    | [`blaze999/Medical-NER`](https://huggingface.co/blaze999/Medical-NER)                                       |
| `french_persons`     | French   | Person                              | [`EmergentMethods/gliner_medium_news-v2.1`](https://huggingface.co/EmergentMethods/gliner_medium_news-v2.1) |
| `french_medical`     | French   | Disease (`Maladie`)                 | [`almanach/camembert-bio-gliner-v0.1`](https://huggingface.co/almanach/camembert-bio-gliner-v0.1)           |

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