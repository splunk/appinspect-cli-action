import json
import sys
import tabulate
from pprint import pprint

class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"

def format_result(result):
    header = result.keys()
    row = [[result[x] for x in result]]
    print(tabulate.tabulate(row, header))   


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
                    print(f'{BCOLORS.OKBLUE}{BCOLORS.BOLD} SUMMARY')
                    format_result(result["summary"])
                    print("::set-output name=status::pass")
                else:
                    print(f"App Inspect returned {failures} failures.")
                    print("::set-output name=status::fail")
                    print(f'{BCOLORS.OKBLUE}{BCOLORS.BOLD} SUMMARY')
                    format_result(result["summary"])
                    print(f'{BCOLORS.OKBLUE}{BCOLORS.BOLD} Failure List:')
                    for group in result["reports"][0]["groups"]:
                        for check in group["checks"]:
                            if check["result"] == "failure":
                                print(f'{BCOLORS.FAIL}check["name"]')
                                for msg in check["messages"]:
                                    print(msg["message"])
                    sys.exit(1)
            else:
                print("Unexpected JSON format")
                print("::set-output name=status::fail")
                sys.exit(1)
    except Exception as e:
        print(f"An error occurred {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    print(sys.argv[1:])
    main(sys.argv[1:])
