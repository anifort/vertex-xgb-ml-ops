#!/usr/bin/env bash
python setup.py test
pip install coverage
rtrn_code=$?
coverage erase
exit $rtrn_code