#!/usr/bin/env bash
python ../setup.py test
rtrn_code=$?
coverage erase
exit $rtrn_code