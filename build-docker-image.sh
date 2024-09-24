#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`

echo "Building ph-eye ${VERSION}..."

docker build --build-arg MODEL_NAME="urchade/gliner_mediumv2.1" -t philterd/ph-eye:${VERSION} .
docker tag philterd/ph-eye:${VERSION} philterd/ph-eye:latest

#docker push philterd/ph-eye:${VERSION}
#docker push philterd/ph-eye:latest
