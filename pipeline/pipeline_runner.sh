#!/usr/bin/env bash
set -e
python setup.py install
python run-pipeline.py -uri $1 -l $2 -pp $3 -pn $4 -pid $5 -ruri $6 -rn $7 -sa $8