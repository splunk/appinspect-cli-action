#!/bin/sh -l
splunk-appinspect --help
splunk-appinspect inspect $1 --output-file appinspect_result.json --mode precert || :
python check.py
