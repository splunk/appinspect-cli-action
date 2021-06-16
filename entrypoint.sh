#!/usr/bin/env bash
#   ########################################################################
#   Copyright 2021 Splunk Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#   ######################################################################## 

if [ -f $INPUT_APP_PATH ]
then 
    SCAN=$INPUT_APP_PATH
else
    ls $INPUT_APP_PATH/
    D=$INPUT_APP_PATH
    files=($D/*)
    SCAN=${files[0]}
fi
echo scan target $SCAN
if [ ! -f $SCAN ]; then echo Unable to locate package $SCAN aborting; exit 1; fi;

if [ ! -z $INPUT_INCLUDED_TAGS ]; then INCLUDED_TAGS="--included-tags ${INPUT_INCLUDED_TAGS}"; fi
if [ ! -z $INPUT_EXCLUDED_TAGS ]; then EXCLUDED_TAGS="--excluded-tags ${INPUT_EXCLUDED_TAGS}"; fi

echo "::group::appinspect"
rm -f $INPUT_RESULT_FILE || true 1>/dev/null
echo running: splunk-appinspect inspect $SCAN --output-file $INPUT_RESULT_FILE --mode test $INCLUDED_TAGS $EXCLUDED_TAGS
splunk-appinspect inspect $SCAN --output-file $INPUT_RESULT_FILE --mode test $INCLUDED_TAGS $EXCLUDED_TAGS
if [ ! -f $INPUT_RESULT_FILE ]; then echo no result file; exit 1; fi
echo "::endgroup::"

echo "::group::reporter"
python3 /reporter.py $INPUT_RESULT_FILE
echo "::endgroup::"