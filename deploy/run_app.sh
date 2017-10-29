#!/bin/bash

if [[ "$MBS2_ENVIRONMENT" = "development" ]]; then
/loop.sh python3 server.py VISIBLE
else
exec uwsgi /etc/uwsgi.ini
fi