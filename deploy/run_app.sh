#!/bin/bash

if [[ "$MBS2_ENVIRONMENT" = "development" ]]; then
python3 server.py VISIBLE
else
nginx
uwsgi /etc/uwsgi.ini
fi