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

MODELS=(pii_base hospitals medical_conditions french_persons french_medical)

for MODEL in "${MODELS[@]}"; do
    TAG="philterd/ph-eye:${VERSION}-${MODEL}"
    echo "Building ${TAG}..."
    docker build --build-arg PHEYE_MODEL="${MODEL}" -t "${TAG}" .
    echo "Built ${TAG}"
done

if [ "$GPU" = true ]; then
    for MODEL in "${MODELS[@]}"; do
        TAG="philterd/ph-eye:${VERSION}-${MODEL}-gpu"
        echo "Building ${TAG}..."
        docker build -f Dockerfile.gpu --build-arg PHEYE_MODEL="${MODEL}" -t "${TAG}" .
        echo "Built ${TAG}"
    done
fi
