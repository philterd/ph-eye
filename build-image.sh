#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`
MODEL_NAME=${1:-"blaze999/Medical-NER"}

echo "Building ph-eye ${VERSION} with model ${MODEL_NAME}"

docker build -t philterd/ph-eye-medical-conditions:${VERSION} .
docker tag philterd/ph-eye-medical-conditions:${VERSION} philterd/ph-eye-medical-conditions:latest
