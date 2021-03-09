# Splunk AppInspect action

This action runs Splunk's AppInspect CLI against a provided a directory of a Splunk App. 
It fails if the result contains any failures.

The (json) result will be written to the file specified under [`result-file`](#result-file).
This can be uploaded for later viewing to use in another step/job using [`actions/upload-artifact@v2`](https://github.com/marketplace/actions/upload-a-build-artifact).

For a more comprehensive Splunk app testing workflow, visit the [`splunk/splunk-app-testing`](https://github.com/splunk/splunk-app-testing) which includes a workflow for cypress testing.


## Inputs

### `app-path`

**Required**: The path to directory of the app in the working directory.

### `result-file`
The file name to use for the json result.
`default`: `appinspect_result.json`

## Outputs

### `status`:  

`pass|fail`

## Example usage

```yml
uses: splunk/appinspect-cli-action@master
with:
  app-path: 'test'
```
