#!/bin/bash -e

VERSION=$(grep -m1 '__version__' app.py | sed 's/.*"\(.*\)".*/\1/')

MODELS=(pii_base hospitals medical_conditions french_persons french_medical)

for MODEL in "${MODELS[@]}"; do
    TAG="philterd/ph-eye:${VERSION}-${MODEL}"
    echo "Pushing ${TAG}..."
    docker push "${TAG}"
    echo "Pushed ${TAG}"
done

for MODEL in "${MODELS[@]}"; do
    TAG="philterd/ph-eye:${VERSION}-${MODEL}-gpu"
    echo "Pushing ${TAG}..."
    docker push "${TAG}"
    echo "Pushed ${TAG}"
done
