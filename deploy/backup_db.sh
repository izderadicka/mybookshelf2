#! /usr/bin/env bash

set -e -o pipefail

TEMP_FILE=/data/tmp/mbs2_db_backup.sql.gz
FINAL_DIR=/data/ebooks

docker compose -f /data/stacks/mbs2/deploy/docker-compose-prod.yml run --rm -T -e PGPASSWORD=$PGPASSWORD db pg_dump -c -h db -U postgres postgres | gzip -c - > $TEMP_FILE

if [[ $? == "0" ]]; then
    chmod 400 $TEMP_FILE
    mv -f $TEMP_FILE $FINAL_DIR
else
    echo "BACKUP FAILURE"
fi