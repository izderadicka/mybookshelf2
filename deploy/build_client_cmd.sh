#!/bin/bash
set -e
cd /code/client
cp /tmp/config.js /code/client/src/config.js
npm install
jspm install -y
export no_proxy=localhost
xvfb-run gulp test
gulp export
