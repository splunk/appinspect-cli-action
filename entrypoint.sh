#!/bin/sh -l

splunk-appinspect inspect $1 --output-file $2 --mode precert > /dev/null

python3 /reporter.py
