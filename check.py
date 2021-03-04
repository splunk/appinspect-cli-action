import json
import sys

def main(args):
    try:
        with open("appinspect_result.json") as f:
            result = json.load(f)
            if result["status"] == "SUCCESS":
                print("::set-output name=status::success")
            print("::set-output name=time::fail")
    except:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
