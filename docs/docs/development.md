# Developer Guide

This guide provides information for developers who want to build, test, or contribute to Ph-Eye.

## Adding a model

1. Create `models/<model_id>.py` implementing the four exports:

   ```python
   DEFAULT_LABELS = [...]      # list of strings
   DEFAULT_THRESHOLD = 0.0     # float

   def load():
       # Download/load the model and return it
       ...

   def predict(model, text, labels, threshold):
       # Run inference and return a list of entity dicts:
       # [{"label": str, "score": float, "text": str, "start": int, "end": int}, ...]
       ...
   ```

2. Add the new `PHEYE_MODEL` value to the `MODELS` array in `build-docker-image.sh` and `push-docker-image.sh`.

## Building Docker images

The `build-docker-image.sh` script reads the version from `app.py` and builds one CPU image and one GPU image per model:

```bash
./build-docker-image.sh
```

This produces tags of the form `philterd/ph-eye:<version>-<model>` (CPU) and `philterd/ph-eye:<version>-<model>-gpu` (GPU). All images are pushed to the same Docker Hub repository.

To build a single CPU image manually:

```bash
docker build --build-arg PHEYE_MODEL=hospitals -t philterd/ph-eye:1.2.5-hospitals .
```

To build a single GPU image manually:

```bash
docker build -f Dockerfile.gpu --build-arg PHEYE_MODEL=hospitals -t philterd/ph-eye:1.2.5-hospitals-gpu .
```

The GPU image uses `pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime` as its base, which provides CUDA 12.1, cuDNN 8, and PyTorch pre-installed. Running a GPU image requires the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) on the host and the `--gpus all` flag.

The build process (both CPU and GPU):

1. Installs dependencies from `requirements.txt`.
2. Copies the `models/` directory into the image.
3. Runs `download_model.py`, which calls `models/<PHEYE_MODEL>.load()` to download and cache the model inside the image.
4. Sets `HF_HUB_OFFLINE=1` so the container uses the cached model at runtime with no outbound network access.

## Testing

After starting the service, run the smoke test:

```bash
./test.sh
```

`test.sh` expects the service to be running on `http://localhost:5000`.

## Environment variables

| Variable                   | Set by               | Description                                                                             |
|----------------------------|----------------------|-----------------------------------------------------------------------------------------|
| `PHEYE_MODEL`              | Dockerfile           | Selects the model module (`models/<value>.py`). Set via `--build-arg` at build time.    |
| `HF_HUB_OFFLINE`           | Dockerfile           | Set to `1` — forces Hugging Face to use the cached model; no network access at runtime. |
| `HF_HUB_DISABLE_TELEMETRY` | Dockerfile           | Set to `1` — disables Hugging Face telemetry.                                           |
| `DO_NOT_TRACK`             | Dockerfile           | Set to `1` — disables general usage tracking.                                           |
| `MODEL_NAME`               | `models/pii_base.py` | Overrides the default Hugging Face model name for the `pii_base` module only.           |
