#!/usr/bin/env python3
"""Run test cases for dagan-utils"""

import json
import os
import subprocess
import sys
import tempfile


def run_testcase(testcase):
    """Run a single testcase"""
    expected_stdout = bytes(testcase["stdout"] + "\n", "ascii")
    command = testcase["run"]
    commands = ["bash", "-c", command]
    result = subprocess.run(commands, check=True, capture_output=True)
    if expected_stdout != result.stdout:
        print("Failed")
        print(f"\tCommand: {command}")
        print(f"\tExpected: {expected_stdout}")
        print(f"\tActual: {result.stdout}")
        sys.exit(1)


def main():
    """Main function"""

    with open("tests/cases.json", encoding="utf-8") as file:
        cases = json.loads(file.read())

    cwd = os.getcwd()
    os.environ["PATH"] += f"{cwd}/bin/"

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
            for case in case["cases"]:
                run_testcase(case)
        else:
            run_testcase(case)

        for file in files:
            os.unlink(file)
        os.chdir(cwd)
        os.rmdir(tempdir)

        count += 1

    print(f"Ran {count} tests")


main()
