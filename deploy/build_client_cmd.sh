#!/bin/bash
set -e

npm install
jspm install -y
xvfb-run gulp test
gulp export
