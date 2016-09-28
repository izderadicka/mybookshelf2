#!/bin/bash
set -e
export $(cat .env | xargs)
IMAGE=mbs2-client-build-image
VOLUME=$CODE_VOLUME
if [[ ${VOLUME:0:1} == "." ]]; then
VOLUME=`pwd`/$VOLUME
fi

docker build -t $IMAGE -f Dockerfile-build-client .
docker run --env-file .env --rm  -it -v $VOLUME:/code $IMAGE /build_client_cmd.sh 
#docker rmi $IMAGE
