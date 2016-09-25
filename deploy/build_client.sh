#!/bin/bash
set -e

IMAGE=mbs2-client-build-image

docker build -t $IMAGE -f Dockerfile-build-client .
docker run --rm  -it -v `pwd`/../client:/client -v `pwd`/config.js:/client/src/config.js $IMAGE /build_client_cmd.sh 

CLIENT_DIR=`pwd`/../client/export

if [[ -d $CLIENT_DIR ]]; then 
echo "Client is build successfully in $CLIENT_DIR"
else
echo "Something went wrong"
fi