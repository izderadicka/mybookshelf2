#!/bin/bash
set -e
export $(cat .env | xargs)
IMAGE=mbs2-client-build-image
VOLUME=$CODE_VOLUME
if [[ ${VOLUME:0:1} == "." ]]; then
VOLUME=`pwd`/$VOLUME
fi

docker build -t $IMAGE -f Dockerfile-build-client .
docker run --rm  --name mbs2-client-watch -it -v $VOLUME:/code -p 9000:9000  $IMAGE /watch_client_cmd.sh 

