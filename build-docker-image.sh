#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`
MODEL_NAME=${1:-"urchade/gliner_mediumv2.1"}

echo "Building ph-eye ${VERSION} with model ${MODEL_NAME}"

docker build --build-arg MODEL_NAME="${MODEL_NAME}" -t philterd/ph-eye:${VERSION} .
docker tag philterd/ph-eye:${VERSION} philterd/ph-eye:latest

docker push philterd/ph-eye:${VERSION}
docker push philterd/ph-eye:latest
