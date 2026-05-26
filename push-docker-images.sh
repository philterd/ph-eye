#!/bin/bash -e
#
# Usage: ./push-docker-images.sh [--no-gpu]
#
#   Pushes one CPU image per model. GPU images are also pushed by default.
#   Pass --no-gpu to skip pushing the GPU images.
#
#   Examples:
#     ./push-docker-images.sh           # pushes CPU + GPU images
#     ./push-docker-images.sh --no-gpu  # pushes CPU images only

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
    echo "Pushing ${TAG}..."
    docker push "${TAG}"
    echo "Pushed ${TAG}"
done

if [ "$GPU" = true ]; then
    for MODEL in "${MODELS[@]}"; do
        TAG="philterd/ph-eye:${VERSION}-${MODEL}-gpu"
        echo "Pushing ${TAG}..."
        docker push "${TAG}"
        echo "Pushed ${TAG}"
    done
fi
