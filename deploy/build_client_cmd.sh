#!/bin/bash
set -e
cd /client
npm install
jspm install -y
xvfb-run gulp test
gulp export
