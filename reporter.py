import json
import sys
from pprint import pprint

def main(args):
    try:
        with open(\"$2\") as f:
            result = json.load(f)
            if \"summary\" in result and \"failure\" in result[\"summary\"]:
                failures = result[\"summary\"][\"failure\"]
                if failures == 0:
                    print(\"App Inspect Passed!\")
                    if \"warning\" in result[\"summary\"] and result[\"summary\"][\"warning\"]:
                        print(\"Warning List:\")
                        for group in result[\"reports\"][0][\"groups\"]:
                            for check in group[\"checks\"]:
                                if check[\"result\"]==\"warning\":
                                    for msg in check[\"messages\"]:
                                        print(msg[\"message\"])
                    pprint(result[\"summary\"])
                    print(\"::set-output name=status::pass\")
                else:
                    print(f\"App Inspect returned {failures} failures.\")
                    print(\"::set-output name=status::fail\")
                    pprint(result[\"summary\"])
                    print(\"Failure List:\")
                    for group in result[\"reports\"][0][\"groups\"]:
                        for check in group[\"checks\"]:
                            if check[\"result\"]==\"failure\":
                                for msg in check[\"messages\"]:
                                    print(msg[\"message\"])
                    sys.exit(1)
            else:
                print(\"Unexpected JSON format\")
                print(\"::set-output name=status::fail\")
                sys.exit(1)
    except Exception as e:
        print(f\"An error occured {str(e)}\")
        sys.exit(1)


if __name__ == \"__main__\":
    main(sys.argv[1:])
