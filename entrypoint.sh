#!/bin/sh -l
splunk-appinspect inspect --help
splunk-appinspect inspect $1 --output-file appinspect_result.json --mode precert || true
python check.py
