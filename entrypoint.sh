#!/bin/sh -l
set +o pipefail

splunk-appinspect inspect --help
splunk-appinspect inspect $1 --output-file appinspect_result.json --mode precert > /dev/null || true
echo "checking status of json result"
python check.py
