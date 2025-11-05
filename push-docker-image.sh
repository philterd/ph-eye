#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`

docker push philterd/ph-eye:${VERSION}
docker push philterd/ph-eye:latest
