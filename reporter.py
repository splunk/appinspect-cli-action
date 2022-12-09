import json
import sys
from pprint import pprint
import os


def main(args):
    try:
        with open(args[0]) as f:
            result = json.load(f)
            if "summary" in result and "failure" in result["summary"]:
                failures = result["summary"]["failure"]
                if failures == 0:
                    print("App Inspect Passed!")
                    if "warning" in result["summary"] and result["summary"]["warning"]:
                        print("Warning List:")
                        for group in result["reports"][0]["groups"]:
                            for check in group["checks"]:
                                if check["result"] == "warning":
                                    for msg in check["messages"]:
                                        print(msg["message"])
                    pprint(result["summary"])
                    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
                        print("status=pass", file=fh)
                else:
                    print(f"App Inspect returned {failures} failures.")
                    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
                        print("status=fail", file=fh)
                    pprint(result["summary"])
                    print("Failure List:")
                    for group in result["reports"][0]["groups"]:
                        for check in group["checks"]:
                            if check["result"] == "failure":
                                for msg in check["messages"]:
                                    print(msg["message"])
                    sys.exit(1)
            else:
                print("Unexpected JSON format")
                with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
                    print("status=fail", file=fh)
                sys.exit(1)
    except Exception as e:
        print(f"An error occurred {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    print(sys.argv[1:])
    main(sys.argv[1:])
