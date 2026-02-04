#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`
MODEL_NAME=${1:-"almanach/camembert-bio-gliner-v0.1"}

echo "Building ph-eye ${VERSION} with model ${MODEL_NAME}"

docker build -t philterd/ph-eye-fr-medical:${VERSION} .
docker tag philterd/ph-eye-fr-medical:${VERSION} philterd/ph-eye-fr-medical:latest
