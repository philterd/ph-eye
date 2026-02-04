#!/bin/bash -e

VERSION=`cat app.py | grep "__version__" | head -1 | tr -d '__version__ = "'`

docker push philterd/ph-eye-fr-persons:${VERSION}
docker push philterd/ph-eye-fr-persons:latest
