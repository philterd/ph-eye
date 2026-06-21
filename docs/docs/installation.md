# Installation and Running

Ph-Eye can be run using Docker or directly from the source code.

## Running with Docker

The easiest way to run Ph-Eye is using an official Docker image. Each image bundles a specific model — select the tag
that matches your use case.

```bash
docker run -p 5000:5000 philterd/ph-eye:1.3.0-pii_en_small
```

The model is baked into the image at build time. No environment variables are needed to select or configure the model at
runtime.

See [Available models](index.md#available-models) for the full list of image tags.

## Running with Docker (GPU)

GPU-enabled images require the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) on the host. Use the `-gpu` image tag and pass `--gpus all`:

```bash
docker run --gpus all -p 5000:5000 philterd/ph-eye:1.3.0-pii_en_small-gpu
```

To run all models together using Docker Compose:

```bash
docker compose -f docker-compose.gpu.yaml up
```

See the [Developer Guide](development.md#building-docker-images) for instructions on building GPU images.

## Building from source

If you need a model not covered by the official images, you can build your own. See
the [Developer Guide](development.md#building-docker-images) for instructions.

## Running from source

### Prerequisites

- Python 3.9+
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/philterd/ph-eye.git
   cd ph-eye
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set the model and run the service:
   ```bash
   PHEYE_MODEL=pii_en_small python app.py
   ```

The service will be available at `http://localhost:5000`.

Note: When running from source, the model is downloaded from Hugging Face on first startup and cached locally.
Subsequent startups use the cached copy.
