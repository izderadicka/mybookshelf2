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

if [[ "$1" == "stage" ]] && [[ ! -f ssl/server.key.pem || ! -f ssl/server.cert.pem ]]; then
    cat << EOF
    For stage environment you need to put server.key.pem and server.cert.pem into ssl directory
    You can generate test selfsigned certificate with openssl:

    openssl req -newkey rsa:2048 -nodes -keyout ssl/server.key.pem -x509 -days 365 -out ssl/server.crt.pem \
    -subj "/C=CZ/ST=Prague/L=Prague/O=Dummy Certificate/CN=localhost"
EOF
exit 1
fi
CURRENT_USER=$(id -u):$(id -g)
read_password "Database password: "  MBS2_DB_PASSWORD

CLIENT_IMAGE=mbs2-client-build-image
docker build -t $CLIENT_IMAGE -f Dockerfile-build-client .

if [[ "$1" = "development" ]]; then
    cat <<EOF >.env
POSTGRES_PASSWORD="$MBS2_DB_PASSWORD"
MBS2_ENVIRONMENT=development
MBS2_DEBUG=true
CODE_VOLUME=..
MBS2_USER=$CURRENT_USER
MBS2_USER_NAME=$USER
EOF
    compose_files=""
elif [[ "$1" = "stage" ]]; then
    cat <<EOF >.env
POSTGRES_PASSWORD="$MBS2_DB_PASSWORD"
MBS2_ENVIRONMENT=stage
MBS2_DEBUG=false
CODE_VOLUME=code
MBS2_USER=10000:0
MBS2_USER_NAME=usak
EOF
    docker run --env-file .env --rm  -it -v code:/code $CLIENT_IMAGE /build_client_cmd.sh 
    compose_files="-f docker-compose.yml -f docker-compose-stage.yml"
else
    echo Uknown environment
    exit 1
fi
export $(cat .env | xargs)
docker build -t mbs2-ubuntu --build-arg MBS2_ENVIRONMENT=$MBS2_ENVIRONMENT .
read_password "Mybookshelf2 admin password: " MBS2_ADMIN_PASSWORD
docker-compose $compose_files up -d db
sleep 3
docker-compose $compose_files run --user $MBS2_USER --rm  app python3 manage.py create_tables -a -c
docker-compose $compose_files run --rm  app python3 manage.py change_password admin -p "$MBS2_ADMIN_PASSWORD"

if [[ "$1" = "development" ]]; then
    #create test database
    cat ../sql/create_test_db.sql |  docker-compose $compose_files run --rm -e PGPASSWORD="$MBS2_DB_PASSWORD" db psql -h db postgres postgres
    cat init_test_db.sql |  docker-compose $compose_files run --rm -e PGPASSWORD="$MBS2_DB_PASSWORD" db psql -h db ebooks_test postgres
    cat <<EOF
#####################################################
Now MyBookself2 is running in developement mode
serving code from local directory.
In browser you can open simple client as http://localhost:6006
and full client with http://localhost:9000

Both client code and server code (apart of backend)
are in watch mode - so any changes are applied immediatelly

To run tests:
docker-compose run --rm app py.test app common
docker-compose run --rm  backend py.test engine
######################################################
EOF
    docker-compose up
    echo
    echo You can restart application with running docker-compose up from this directory
elif [[ "$1" = "stage" ]]; then
    docker-compose $compose_files  up -d
    cat << EOF
Now stage deployment is running in background.
You can access full client on https://localhost:4443/client/
and lite client on https://localhost:4443
EOF
fi




