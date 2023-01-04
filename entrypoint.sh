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
exit_code=$?
echo "::endgroup::"

exit_code_failure_check=$exit_code
if [ $exit_code != 0 ]; then
  echo "::group::failure_checks"
  python3 /compare_checks.py $INPUT_APPINSPECT_EXPECTED_FAILURES $INPUT_RESULT_FILE "failure"
  exit_code_failure_check=$?
  echo "::endgroup::"
fi

echo "::group::manual_checks"
python3 /compare_checks.py $INPUT_APPINSPECT_MANUAL_CHECKS $INPUT_RESULT_FILE "manual_check"
exit_code_manual_check=$?
echo "::endgroup::"

if [ $exit_code_failure_check == 0 ] && [ $exit_code_manual_check == 0 ] ; then
  echo "::group::generate_markdown"
  echo "successful comparison, generating markdown"
  python3 /export_to_markdown.py $INPUT_APPINSPECT_MANUAL_CHECKS $INPUT_MANUAL_CHECK_MARKDOWN
  python3 /export_to_markdown.py $INPUT_APPINSPECT_EXPECTED_FAILURES $INPUT_EXPECTED_FAILURE_MARKDOWN
  echo "::endgroup::"
fi

exit "$(($exit_code_failure_check || $exit_code_manual_check))"
