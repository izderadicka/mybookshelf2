#!/bin/bash
set -e -x
cp -av /tmp/code/client /code
cp -av /tmp/code/app/static /dist/

cd /code/client
sed -i -r 's/"port": (6006|8080)/"port": null/g' src/config.js
npm install
# if you have problem with reaching github API limit use line below
#jspm config registries.github.auth your_github_token
jspm install -y
# running test - require to install xvfb , which is now not available for old base image
# export no_proxy=localhost
# xvfb-run gulp test
gulp export

cp -av ./export /dist/
