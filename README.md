# Splunk AppInspect action

This action runs Splunk's AppInspect CLI against a provided a directory of a Splunk App. 
It fails if the result contains any failures.

The (json) result will be written to the file specified with [`result-file`](#result-file).
This can be uploaded for later viewing to use in another step/job using [`actions/upload-artifact@v2`](https://github.com/marketplace/actions/upload-a-build-artifact).

For a more comprehensive Splunk app testing workflow, visit the [`splunk/splunk-app-testing`](https://github.com/splunk/splunk-app-testing) which includes a workflow for cypress testing.


## Inputs

### `app_path`

**Required**: The path to directory of the app in the working directory.

### `result-file`
The file name to use for the json result.
`default`: `appinspect_result.json`

## Outputs

### `status`:  

`pass|fail`

## Example usage

```yml
uses: splunk/appinspect-cli-action@v1
with:
  app_path: 'test'
```

## Using manual tag
Running `appinspect-cli-action` with `manual` tag in `included_tags` detects checks that need to be verified manually and tests if all of them were already reviewed - if not the action will fail.
### manual checks review
To see checks to be verified inspect the `result_file` from `appinspect-cli-action` run with manual tag. Verify manual checks and mark them as reviewed by adding them one by one into `.app-vetting.yaml`, ex:
```
name_of_manual_check_1:
  comment: 'your comment'
name_of_manual_check_2:
  comment: 'your comment'
```
please note that names of validated manual checks should be aligned with those from appinspect output and your comment can't be empty.
### running the job
When job is ran with manual tag it scans the package with appinspect and searches for manual checks. In next step compares appinspect's results with `.app-vetting.yaml` if any check wasn't reviewed and isn't in `.app-vetting.yaml` then the job fails.
#### downloading manual checks markdwon
If the comparison is successful then a markdown consisting a table with manual check names and comments is generated. It can be uploaded to artifacts.
```
- name: upload-manual-check-markodown
        uses: actions/upload-artifact@v2
        with:
          name: manual_check_markdown.txt
          path: manual_check_markdown.txt
```
The markdown is ready to paste into confluence, by:
`Edit -> Insert more content -> Markup`, change insert type to `Markdown` and paste the contents of the file