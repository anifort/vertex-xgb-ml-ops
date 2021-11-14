#!/usr/bin/env bash
set -e
python setup.py install
python src/compile-pipeline.py -d $1