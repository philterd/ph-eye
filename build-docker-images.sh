#!/bin/bash -e
#
# Usage: ./build-docker-images.sh [--no-gpu]
#
#   Builds one CPU image per model. GPU images are also built by default.
#   Pass --no-gpu to skip building the GPU images.
#
#   Examples:
#     ./build-docker-images.sh           # builds CPU + GPU images
#     ./build-docker-images.sh --no-gpu  # builds CPU images only

GPU=true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-gpu) GPU=false ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

VERSION=$(grep -m1 '__version__' app.py | sed 's/.*"\(.*\)".*/\1/')

MODELS=(pii_en_small pii_en_xsmall pii_en_medium pii_en_large pii_base hospitals medical_conditions french_persons french_medical)

# The default English model. Its CPU image is also tagged "latest" and its GPU
# image "latest-gpu" so a plain `docker pull philterd/ph-eye` gets the default.
DEFAULT_MODEL=pii_en_small

for MODEL in "${MODELS[@]}"; do
    TAG="philterd/ph-eye:${VERSION}-${MODEL}"
    echo "Building ${TAG}..."
    docker build --build-arg PHEYE_MODEL="${MODEL}" -t "${TAG}" .
    echo "Built ${TAG}"
    if [ "$MODEL" = "$DEFAULT_MODEL" ]; then
        docker tag "${TAG}" "philterd/ph-eye:latest"
        echo "Tagged philterd/ph-eye:latest -> ${TAG}"
    fi
done

if [ "$GPU" = true ]; then
    for MODEL in "${MODELS[@]}"; do
        TAG="philterd/ph-eye:${VERSION}-${MODEL}-gpu"
        echo "Building ${TAG}..."
        docker build -f Dockerfile.gpu --build-arg PHEYE_MODEL="${MODEL}" -t "${TAG}" .
        echo "Built ${TAG}"
        if [ "$MODEL" = "$DEFAULT_MODEL" ]; then
            docker tag "${TAG}" "philterd/ph-eye:latest-gpu"
            echo "Tagged philterd/ph-eye:latest-gpu -> ${TAG}"
        fi
    done
fi
