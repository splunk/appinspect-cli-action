# Splunk AppInspect action

This action runs Splunk's AppInspect CLI against a provided directory of Splunk App. 
It fails if the result contains any failures or manual checks are not vetted.

The (json) result will be written to the file specified with [`result-file`](#result-file).
This can be uploaded for later viewing to use in another step/job using [`actions/upload-artifact@v2`](https://github.com/marketplace/actions/upload-a-build-artifact).

For a more comprehensive Splunk app testing workflow, visit the [`splunk/splunk-app-testing`](https://github.com/splunk/splunk-app-testing) which includes a workflow for cypress testing.

## Inputs

### `app_path`

**Required**: The path to directory of the app in the working directory.

### `result-file`
The file name to use for the json result.

`default`: `appinspect_result.json`

### `included_tags`
Appinspect tags to include

`required`: `false`
  
### `excluded_tags`
Appinspect tags to exclude

`required`: `false`

### `appinspect_manual_checks`
Path to file which contains list of manual checks

`required`: `false`
`default`: `.appinspect.manualcheck`

### `appinspect_expected_failures`
Path to file which contains list of expected appinspect failures

`required`: `false`
`default`: `.appinspect.expect`

### `manual_check_markdown`
Path to generated file with markdown for manual checks

`required`: `false`
`default`: `manual_check_markdown.txt`

### `appinspect_expected_failures`
Path to generated file with markdown for expected appinspect failures

`required`: `false`
`default`: `expected_failure_markdown.txt`

## Outputs

### `status`:  

`pass|fail`

### Manual checks review
To see checks to be verified, inspect the `result_file` from `appinspect-cli-action`. Verify manual checks and mark them as reviewed by adding them one by one into `.appinspect.manualcheck`, ex:
```yml
name_of_manual_check_1:
  comment: 'your comment'
name_of_manual_check_2:
  comment: 'your comment'
```
Please note that names of validated manual checks should be aligned with those from `result_file` and your comment can't be empty.

### Failure checks review 
To mark Failures as expected, add them into `.appinspect.expect` with proper comment containing ticket id of ADDON/APPCERT project associated with the exception, ex:
```yml
name_of_exception_1:
  comment: 'ADDON-123: your comment'
name_of_exception_2:
  comment: 'APPCERT-123: your comment'
```
Please note that your comment can't be empty, it must include ticket id of ADDON/APPCERT project associated with the exception and the names of exceptions should be aligned with those from `result_file`.

### Running the job
When `appinspect-cli-action` is called, it scans the package with Splunk's AppInspect CLI. If there are any failures observed then action compares `results_file` with `.appinspect.expect`. If that failure isn't present in `appinspect.expect` or it does not contain an appropriate comment(containing ADDON/APPCERT ticket id associated with the exception) then the job fails with proper failure reason. In the next step, action compares `results_file` with `.appinspect.manualcheck`. If any manual check wasn't reviewed and isn't in `.appinspect.manualcheck` then the job fails.

## Example usage

```yml
- uses: splunk/appinspect-cli-action@v1
  with:
    app_path: 'test'
```
### Downloading markdowns
If the comparison is successful then a markdown consisting a table with check names and comments is generated. It can be uploaded to artifacts.
```yml
- uses: actions/checkout@v2
- uses: splunk/appinspect-cli-action@v1.3
  with:
    app_path: 'test'
    included_tags: cloud
    manual_check_markdown: manual_check_markdown.txt
    expected_failure_markdown: expected_failure_markdown.txt
- name: upload-manual-check-markodown
  uses: actions/upload-artifact@v2
  with:
    name: manual_check_markdown.txt
    path: manual_check_markdown.txt
- name: upload-expected_failure-markodown
  uses: actions/upload-artifact@v2
  with:
    name: expected_failure_markdown.txt
    path: expected_failure_markdown.txt
```
The markdown is ready to paste into confluence, by:
`Edit -> Insert more content -> Markup`, change insert type to `Markdown` and paste the contents of the file.
