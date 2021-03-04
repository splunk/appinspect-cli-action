import json
import sys

def main(args):
    try:
        with open("appinspect_result.json") as f:
            result = json.load(f)
            if "summary" in result and "failure" in result["summary"]:
                failures = result["summary"]["failure"]
                if failures == 0:
                    print("No Failures")
                    print("::set-output name=status::success")
                else:
                    print(f"App Inspect failed; {failures} failures.")
                    print("::set-output name=time::fail")
                    sys.exit(1)
            else:
                print("Unexpected JSON format")
                sys.exit(1)
    except Exception as e:
        print(f"An error occured {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
