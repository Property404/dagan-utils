#!/usr/bin/env python3
"""Run test cases for dagan-utils"""

import json
import os
import subprocess
import sys
import tempfile


def run_testcase(testcase):
    """Run a single testcase"""
    command = testcase["run"]
    commands = ["bash", "-c", command]

    try:
        result = subprocess.run(commands, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        result = exc
    except Exception as exception:
        raise exception

    if "stdout" in testcase:
        valid = True
        expected_stdout = bytes(testcase["stdout"] + "\n", "ascii")
        if expected_stdout != result.stdout:
            print("Failed")
            print(f"\tCommand: {command}")
            print(f"\tExpected: {expected_stdout}")
            print(f"\tActual: {result.stdout}")
            sys.exit(1)

    if "exit" in testcase:
        valid = True
        expected_exit_status = int(testcase["exit"])
        if expected_exit_status != result.returncode:
            print("Failed")
            print(f"\tCommand: {command}")
            print(f"\tExpected status: {expected_exit_status}")
            print(f"\tActual status: {result.returncode}")
            sys.exit(1)
    elif result.returncode != 0:
        print("Failed")
        print(f"\tCommand: {command}")
        print(f"\tStatus: {result.returncode}")
        sys.exit(1)

    if not valid:
        print("Test case does not test anything!")
        sys.exit(1)


def main():
    """Main function"""

    with open("tests/cases.json", encoding="utf-8") as file:
        cases = json.loads(file.read())

    cwd = os.getcwd()
    os.environ["PATH"] = f"{cwd}/bin/:{os.environ['PATH']}"

    count = 0
    for case in cases:
        tempdir = tempfile.mkdtemp()
        os.chdir(tempdir)

        files = []
        if "files" in case:
            files = case["files"]
            for filename in files:
                with open(filename, "wb") as file:
                    contents = files[filename]
                    file.write(bytes(contents.encode("ascii")))

        if "cases" in case:
            for subcase in case["cases"]:
                run_testcase(subcase)
        else:
            run_testcase(case)

        for file in files:
            os.unlink(file)
        os.chdir(cwd)
        os.rmdir(tempdir)

        count += 1

    print(f"Ran {count} tests")


main()
