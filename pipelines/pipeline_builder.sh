#!/usr/bin/env bash
set -e
python setup.py install
python compile-pipeline.py -d $1 -pt $2