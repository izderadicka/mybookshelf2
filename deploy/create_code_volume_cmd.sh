#!/bin/bash
set -e
rm -r /code/*
git clone --depth 1 https://github.com/izderadicka/mybookshelf2 /tmp/code
rm -rf /tmp/code/.git /tmp/code/data /tmp/code/tests /tmp/code/tools
mv /tmp/code/* .
rm -r /tmp/code