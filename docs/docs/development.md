# Developer Guide

This guide provides information for developers who want to build, test, or contribute to Ph-Eye.

## Project Structure

- `app.py`: The main Flask application.
- `download-model.py`: Script to pre-download a GLiNER model.
- `Dockerfile`: Docker configuration for building the Ph-Eye image.
- `build-docker-image.sh`: Helper script to build and tag the Docker image.
- `run.sh`: Script used inside the Docker container to start the service.
- `test.sh`: A simple script to test the `/find` endpoint.

## Building the Docker Image

You can build the Docker image using the provided `build-docker-image.sh` script:

```bash
./build-docker-image.sh [MODEL_NAME]
```

If `MODEL_NAME` is not provided, it defaults to `philterd/ph-eye-pii-base`.

The build process includes:
1. Installing dependencies from `requirements.txt`.
2. Running `download-model.py` to bake the model into the image (controlled by the `MODEL_NAME` build argument).
3. Setting environment variables to disable telemetry and enable offline mode for Hugging Face Hub.

## Testing

After starting the service (either via Docker or from source), you can run the `test.sh` script to verify it's working:

```bash
./test.sh
```

Note: `test.sh` expects the service to be running on `http://localhost:18080`. If you are running on a different port, you will need to modify the script or run the `curl` command manually.

## Environment Variables

When developing or running Ph-Eye, the following environment variables are used:

- `MODEL_NAME`: The GLiNER model to load.
- `HF_HUB_DISABLE_TELEMETRY`: Set to `1` to disable Hugging Face telemetry.
- `HF_HUB_OFFLINE`: Set to `1` in the Docker image to ensure it uses the pre-downloaded model.
- `DO_NOT_TRACK`: Set to `1` to disable tracking.
