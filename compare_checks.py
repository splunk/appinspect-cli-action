import json
import os
import sys
from typing import List

import yaml

print(
    f"{os.path.basename(__file__)} script was called with parameters: {' '.join(sys.argv[1:])}"
)
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
    if not os.path.isfile(appinspect_result_file):
        raise FileNotFoundError(
            f"File {appinspect_result_file} does not exist. Something went wrong with report generation"
        )

    manual_checks = get_checks_from_appinspect_result(appinspect_result_file)
    failure_checks = get_checks_from_appinspect_result(appinspect_result_file,result="failure")
    
    vetting_data = {}
    if os.path.isfile(vetting_file):
        with open(vetting_file) as f:
            vetting_data = yaml.safe_load(f)
    if len(vetting_data) == 0:
        if manual_checks:
            print(
                f"{BCOLORS.WARNING}{BCOLORS.BOLD}{vetting_file} is empty. You can initilize it with below yaml content."
                f" Every check requires some comment which means that check was manually verified{BCOLORS.ENDC}"
            )
            for check in manual_checks:
                print(f"{BCOLORS.WARNING}{BCOLORS.BOLD}{check}:{BCOLORS.ENDC}")
                print(f"{BCOLORS.WARNING}{BCOLORS.BOLD}  comment: ''{BCOLORS.ENDC}")
            print()

    new_manual_checks = list(set(manual_checks) - set(vetting_data.keys()))
    new_failure_checks = list(set(failure_checks) - set(vetting_data.keys()))
    print(new_failure_checks)
    
    if new_manual_checks:
        print(
            f"{BCOLORS.FAIL}{BCOLORS.BOLD}Some manual checks were found in appinspect output, which are not present in"
            f" {vetting_file}. List of checks:{BCOLORS.ENDC}"
        )
        for check in new_manual_checks:
            print(f"{BCOLORS.FAIL}{BCOLORS.BOLD}\t{check}{BCOLORS.ENDC}")

    if new_failure_checks:
        print(
            f"{BCOLORS.FAIL}{BCOLORS.BOLD}Some failure checks were found in appinspect output, if these issues have approved exceptions update the vetting file"
            f" {vetting_file}. List of checks:{BCOLORS.ENDC}"
        )
        for check in new_failure_checks:
            print(f"{BCOLORS.FAIL}{BCOLORS.BOLD}\t{check}{BCOLORS.ENDC}")

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

    if new_manual_checks or not_commented:
        print(
            f"{BCOLORS.FAIL}{BCOLORS.BOLD}Please see appinspect report for more detailed description about manual checks and review them accordingly.{BCOLORS.ENDC}"
        )

    return new_manual_checks + new_failure_checks + not_commented


def get_checks_from_appinspect_result(path: str,result: str="manual_check") -> List[str]:
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
                    if check["result"] == result:
                        manual_checks.append(check["name"])
    return manual_checks


def main():
    not_verified_checks = compare(APP_VETTING_PATH, APPINSPECT_OUTPUT_PATH)
    if not_verified_checks:
        exit(1)


if __name__ == "__main__":
    main()
