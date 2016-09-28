#!/bin/bash
set -e
cd /code/client
npm install
jspm install -y
gulp watch
