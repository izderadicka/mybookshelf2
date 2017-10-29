#!/bin/bash
set -e -x
function read_password {

eval local existing=\$$2
if [[ -z "$existing" ]]; then
    read -p "$1" $2
    local pwd1
    read -p "Enter password again for check: " pwd1
    eval local pwd0=\$$2 
    if [[ ! "$pwd1" = "$pwd0" ]]; then
        echo "Passwords were different"
        exit 1
    fi
fi

}

if [[ -z "$1" ]]; then 
    echo Usage: $0 [development|stage]
    exit 1
fi
CURRENT_USER=$(id -u):$(id -g)
read_password "Database password: "  MBS2_DB_PASSWORD

if [[ "$1" = "development" ]]; then
    cat <<EOF >.env
POSTGRES_PASSWORD="$MBS2_DB_PASSWORD"
MBS2_ENVIRONMENT=development
MBS2_DEBUG=true
CODE_VOLUME=..
MBS2_USER=$CURRENT_USER
MBS2_USER_NAME=$USER
EOF
elif [[ "$1" = "stage" ]]; then
    cat <<EOF >.env
POSTGRES_PASSWORD="$MBS2_DB_PASSWORD"
MBS2_ENVIRONMENT=development
MBS2_DEBUG=true
CODE_VOLUME=..
MBS2_USER=$CURRENT_USER

EOF
else
    echo Uknown environment
    exit 1
fi
export $(cat .env | xargs)
docker build -t mbs2-ubuntu .
read_password "Mybookshelf2 admin password: " MBS2_ADMIN_PASSWORD
docker-compose up -d db
sleep 3
docker-compose run --user $MBS2_USER --rm  app python3 manage.py create_tables -a -c
docker-compose run --rm  app python3 manage.py change_password admin -p "$MBS2_ADMIN_PASSWORD"

CLIENT_IMAGE=mbs2-client-build-image
docker build -t $CLIENT_IMAGE -f Dockerfile-build-client .
if [[ "$1" = "development" ]]; then

    cat <<EOF
#####################################################
Now MyBookself2 is running in developement mode
serving code from local directory.
In browser you can open simple client as http://localhost:6006
and full client with http://localhost:9000

Both client code and server code (apart of backend)
are in watch mode - so any changes are applied immediatelly
######################################################
EOF
    docker-compose up
    echo
    echo You can restart application with running docker-compose up from this directory
fi




