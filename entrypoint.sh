#!/bin/sh -l

splunk-appinspect inspect $1 --output-file appinspect_result.json --mode precert
python check.py
