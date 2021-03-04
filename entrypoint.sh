#!/bin/sh -l

splunk-appinspect inspect --help
splunk-appinspect inspect $1 --output-file appinspect_result.json --mode precert > /dev/null || true
ls -ltr
echo "checking status of json result"
python check.py
