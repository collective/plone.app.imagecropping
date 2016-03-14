#!/bin/sh
virtualenv --clear .
./bin/pip install -U pip setuptools zc.buildout
./bin/buildout $*
