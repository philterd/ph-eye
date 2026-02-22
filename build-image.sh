#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`

docker build -t philterd/ph-eye-hospitals:${VERSION} .
docker tag philterd/ph-eye-hospitals:${VERSION} philterd/ph-eye-hospitals:latest
