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

MODELS=(pii_en_small pii_en_xsmall pii_en_medium pii_en_large pii_base hospitals medical_conditions french_persons french_medical)

# The default English model. Its CPU image is also pushed as "latest" and its
# GPU image as "latest-gpu" (see build-docker-images.sh).
DEFAULT_MODEL=pii_en_small

for MODEL in "${MODELS[@]}"; do
    TAG="philterd/ph-eye:${VERSION}-${MODEL}"
    echo "Pushing ${TAG}..."
    docker push "${TAG}"
    echo "Pushed ${TAG}"
done

echo "Pushing philterd/ph-eye:latest (-> ${VERSION}-${DEFAULT_MODEL})..."
docker push "philterd/ph-eye:latest"
echo "Pushed philterd/ph-eye:latest"

if [ "$GPU" = true ]; then
    for MODEL in "${MODELS[@]}"; do
        TAG="philterd/ph-eye:${VERSION}-${MODEL}-gpu"
        echo "Pushing ${TAG}..."
        docker push "${TAG}"
        echo "Pushed ${TAG}"
    done

    echo "Pushing philterd/ph-eye:latest-gpu (-> ${VERSION}-${DEFAULT_MODEL}-gpu)..."
    docker push "philterd/ph-eye:latest-gpu"
    echo "Pushed philterd/ph-eye:latest-gpu"
fi
