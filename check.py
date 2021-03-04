import json
import sys
from pprint import pprint

def main(args):
    try:
        with open("appinspect_result.json") as f:
            result = json.load(f)
            pprint(result)
            if "status" in result and result["status"] == "SUCCESS":
                print("::set-output name=status::success")
            print("::set-output name=time::fail")
    except Exception as e:
        print(f"error occured {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
