import json
import os
import sys

import yaml

from typing import List

APP_VETTING_PATH = sys.argv[1]
APPINSPECT_OUTPUT_PATH = sys.argv[2]


class BCOLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def compare(vetting_file: str = ".app-vetting.yaml", appinspect_result_file: str = "appinspect_output.json") -> List[
    str]:
    """
    Compares checks from vetting file and appinspect result file
    :param vetting_file: path to yaml file with verified manual checks
    :param appinspect_result_file: path to Splunk's AppInspect CLI result file
    :return: list of non matching tests between vetting_file and appinspect_result_file
    """
    if not os.path.isfile(vetting_file):
        raise FileNotFoundError(
            f"{BCOLORS.FAIL}File {vetting_file} does not exist. Create it and fill out with list of verified manual checks{BCOLORS.ENDC}")

    if not os.path.isfile(appinspect_result_file):
        raise FileNotFoundError(
            f"{BCOLORS.FAIL}File {appinspect_result_file} does not exist. Something went wrong with report generation{BCOLORS.ENDC}")

    with open(vetting_file) as f:
        vetting_data = yaml.safe_load(f)

    with open(appinspect_result_file) as f:
        appinspect_results = json.load(f)
        manual_checks = []
        for report in appinspect_results["reports"]:
            for group in report["groups"]:
                for check in group["checks"]:
                    if check["result"] == "manual_check":
                        manual_checks.append(check["name"])

    new_checks = list(set(manual_checks) - set(vetting_data.keys()))
    deprecated_checks = vetting_data.keys() - manual_checks
    if new_checks:
        check_list_to_print = "\n\t".join(new_checks)
        print(
            f"{BCOLORS.FAIL}Some manual checks were found in appinspect output, which are not present in {vetting_file}. List of checks:{BCOLORS.ENDC}")
        print(f"{BCOLORS.FAIL}\t{check_list_to_print}{BCOLORS.ENDC}")
    if deprecated_checks:
        check_list_to_print = "\n\t".join(deprecated_checks)
        print(
            f"{BCOLORS.WARNING}Some manual checks were found in {vetting_file}, which are not present in appinspect output. Please delete them, as they are deprecated. List of checks:{BCOLORS.ENDC}")
        print(f"{BCOLORS.WARNING}\t{check_list_to_print}{BCOLORS.ENDC}")
    return new_checks


def main():
    not_verified_checks = compare(APP_VETTING_PATH, APPINSPECT_OUTPUT_PATH)
    if not_verified_checks:
        exit(1)


if __name__ == '__main__':
    main()
