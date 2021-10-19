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

### `included_tags`
Appinspect tags to include
`required`: `false`
  
### `excluded_tags`
Appinspect tags to exclude
`required`: `false`

### `app_vetting`
Path to app vetting yaml file. Used only if `manual` in `included_tags`
`default`: `.app-vetting.yaml`

### `app_vetting`
Path for generated file with markdown for manual checks. Used only if `manual` in `included_tags`
`default`: `manual_check_markdown.txt`

## Outputs

### `status`:  

`pass|fail`

## Example usage

```yml
uses: splunk/appinspect-cli-action@v1
with:
  app_path: 'test'
```
### Downloading manual checks markdown
If the comparison is successful then a markdown consisting a table with manual check names and comments is generated. It can be uploaded to artifacts.
```yml
- name: upload-manual-check-markodown
        uses: actions/upload-artifact@v2
        with:
          name: manual_check_markdown.txt
          path: manual_check_markdown.txt
```
The markdown is ready to paste into confluence, by:
`Edit -> Insert more content -> Markup`, change insert type to `Markdown` and paste the contents of the file

## Using manual tag
Running `appinspect-cli-action` with `manual` tag in `included_tags` detects checks that need to be verified manually and tests if all of them were already reviewed - if not the action will fail.
### Manual checks review
To see checks to be verified inspect the `result_file` from `appinspect-cli-action` run with manual tag. Verify manual checks and mark them as reviewed by adding them one by one into `.app-vetting.yaml`, ex:
```yml
name_of_manual_check_1:
  comment: 'your comment'
name_of_manual_check_2:
  comment: 'your comment'
```
please note that names of validated manual checks should be aligned with those from `result_file` and your comment can't be empty.
### Running the job
When `appinspect-cli-action` is called with `manual` tag, it scans the package with Splunk's AppInspect CLI and searches for manual checks. In the next step, action compares `results_file` with `.app-vetting.yaml` if any check wasn't reviewed and isn't in `.app-vetting.yaml` then the job fails.
