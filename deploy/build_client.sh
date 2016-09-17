#!/bin/bash
set -e

IMAGE=mbs2-client-build-image

docker build -t $IMAGE -f Dockerfile-build-client .
docker run --rm  -it -v `pwd`/../client:/client $IMAGE /build_client_cmd.sh 

CLIENT_DIR=`pwd`/../client/export

echo "Client is build successfully in $CLIENT_DIR"