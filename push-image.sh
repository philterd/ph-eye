#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`

docker push philterd/ph-eye-medical-conditions:${VERSION}
docker push philterd/ph-eye-medical-conditions:latest
