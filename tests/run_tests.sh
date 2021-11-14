#!/usr/bin/env bash
pip install coverage
rtrn_code=$?
coverage erase
exit $rtrn_code