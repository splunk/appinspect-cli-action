import json
import os
import sys

import yaml

from typing import List

print(f"{os.path.basename(__file__)} script was called with parameters: {' '.join(sys.argv[1:])}")
APP_VETTING_PATH = sys.argv[1]
APPINSPECT_OUTPUT_PATH = sys.argv[2]


class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def compare(
    vetting_file: str = ".app-vetting.yaml",
    appinspect_result_file: str = "appinspect_output.json",
) -> List[str]:
    """
    Compares checks from vetting file and appinspect result file. A lot prints are added to make it
    easier for users to create proper vetting_file and understand errors

    :param vetting_file: path to yaml file with verified manual checks
    :param appinspect_result_file: path to Splunk's AppInspect CLI result file
    :return: list of non matching tests between vetting_file and appinspect_result_file or not commented ones
    """
    if not os.path.isfile(vetting_file):
        raise FileNotFoundError(
            f"File {vetting_file} does not exist. Create it and fill out with list of verified manual checks"
        )

    if not os.path.isfile(appinspect_result_file):
        raise FileNotFoundError(
            f"File {appinspect_result_file} does not exist. Something went wrong with report generation"
        )

    manual_checks = get_checks_from_appinspect_result(appinspect_result_file)

    with open(vetting_file) as f:
        vetting_data = yaml.safe_load(f)
    if vetting_data is None:
        if manual_checks:
            print(f"{vetting_file} is empty. You can initilize it with below yaml content. Every check requires"
                  f"some comment whcih means that check was manually verified")
            for check in manual_checks:
                print(f"{BCOLORS.WARNING}{BCOLORS.BOLD}{check}:{BCOLORS.ENDC}")
                print(f"{BCOLORS.WARNING}{BCOLORS.BOLD}  comment: ''{BCOLORS.ENDC}")
        vetting_data = {}

    new_checks = list(set(manual_checks) - set(vetting_data.keys()))
    deprecated_checks = vetting_data.keys() - manual_checks

    if new_checks:
        print(
            f"{BCOLORS.FAIL}{BCOLORS.BOLD}Some manual checks were found in appinspect output, which are not present in"
            f" {vetting_file}. List of checks:{BCOLORS.ENDC}"
        )
        for check in new_checks:
            print(f"{BCOLORS.FAIL}{BCOLORS.BOLD}\t{check}{BCOLORS.ENDC}")

    if deprecated_checks:
        print(
            f"{BCOLORS.WARNING}{BCOLORS.BOLD}Some manual checks were found in {vetting_file}, which are not present in"
            f" appinspect output. Please delete them, as they are deprecated. List of checks:{BCOLORS.ENDC}"
        )
        for check in deprecated_checks:
            print(f"{BCOLORS.WARNING}{BCOLORS.BOLD}\t{check}{BCOLORS.ENDC}")
    not_commented = []

    for check, info in vetting_data.items():
        if not info.get("comment"):
            not_commented.append(check)

    if not_commented:
        print(
            f"{BCOLORS.FAIL}{BCOLORS.BOLD}All verified manual checks require comment. Below checks are not commented in"
            f" {vetting_file}:{BCOLORS.ENDC}"
        )
        for check in not_commented:
            print(f"{BCOLORS.FAIL}{BCOLORS.BOLD}\t{check}{BCOLORS.ENDC}")

    return new_checks + not_commented


def get_checks_from_appinspect_result(path: str) -> List[str]:
    """
    Returns manual checks from appinspect json result file

    :param path: path to json result file
    :return: list of checks in string format
    """
    manual_checks = []
    with open(path) as f:
        appinspect_results = json.load(f)
        for report in appinspect_results["reports"]:
            for group in report["groups"]:
                for check in group["checks"]:
                    if check["result"] == "manual_check":
                        manual_checks.append(check["name"])
    return manual_checks


def main():
    not_verified_checks = compare(APP_VETTING_PATH, APPINSPECT_OUTPUT_PATH)
    if not_verified_checks:
        exit(1)


if __name__ == "__main__":
    main()
