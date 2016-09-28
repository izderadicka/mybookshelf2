#!/bin/bash

docker build -t mbs2-create-volume -f Dockerfile-create-code-volume .
docker run -v code:/code -t --rm mbs2-create-volume
docker rmi mbs2-create-volume