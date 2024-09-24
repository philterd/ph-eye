#!/bin/bash -e

VERSION=`cat pheye.py | grep "__version__" | tr -d '__version__ = "'`

echo "Building ph-eye ${VERSION}..."

docker build -t philterd/ph-eye:${VERSION} .
docker tag philterd/ph-eye:latest philterd/ph-eye:${VERSION}

docker push philterd/ph-eye:${VERSION} 
docker push philterd/ph-eye:latest
