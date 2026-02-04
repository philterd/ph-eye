#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`
MODEL_NAME=${1:-"EmergentMethods/gliner_medium_news-v2.1"}

echo "Building ph-eye ${VERSION} with model ${MODEL_NAME}"

docker build -t philterd/ph-eye-fr-persons:${VERSION} .
docker tag philterd/ph-eye-fr-persons:${VERSION} philterd/ph-eye-fr-persons:latest
