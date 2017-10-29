#!/bin/bash
set -e -x
rm -r /code/* || true
git clone --depth 1 -b ${MBS2_BRANCH:-master}  https://github.com/izderadicka/mybookshelf2 /tmp/code
rm -rf /tmp/code/.git /tmp/code/data /tmp/code/tests /tmp/code/tools /tmp/code/deploy
mv /tmp/code/* /code
rm -r /tmp/code

cd /code/client
sed -i -r 's/"port": (6006|8080)/"port": null/g' src/config.js
npm install
jspm install -y
export no_proxy=localhost
xvfb-run gulp test
gulp export
