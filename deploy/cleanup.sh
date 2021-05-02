#!/bin/bash
set -e -x

if [[ ! -f .env ]]; then
    echo "init.sh script was not run (no .env file), exiting"
    exit 1
fi

cat <<EOF
This script will clean all docker artifacts (images, volumes, containers ...) from deployment.
ALL DATA WILL BE LOST!
Do you want to continue?
EOF

read -p "Enter y to continue: " ans

if [[ $ans != "y" ]]; then
exit 0
fi


export $(cat .env | xargs)

if [[ $MBS2_ENVIRONMENT == developement ]]; then
    compose_files=""
elif [[ $MBS2_ENVIRONMENT == stage ]]; then
    compose_files="-f docker-compose.yml -f docker-compose-stage.yml"
else
    echo Uknown environment - exiting
    exit 1
fi

echo Starting cleanup of $MBS2_ENVIRONMENT environment

docker-compose $compose_files down --rmi all -v
docker rmi `docker images -f "reference=mbs2*" -q`

if [[ $MBS2_ENVIRONMENT == stage ]]; then
    docker volume rm code
fi

rm .env