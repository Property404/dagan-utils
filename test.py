#!/usr/bin/env python3
"""Run test cases for dagan-utils"""

import json
import subprocess
import tempfile
import os


def main():
    """Main function"""

    with open("tests/cases.json", encoding="utf-8") as file:
        cases = json.loads(file.read())

    cwd = os.getcwd()
    os.environ["PATH"] += f"{cwd}/bin/"
    tempdir = tempfile.mkdtemp()
    os.chdir(tempdir)

    count = 0
    for case in cases:
        expected_stdout = bytes(case["output"] + "\n", "ascii")
        command = case["run"]
        commands = ["bash", "-c", command]
        result = subprocess.run(commands, check=True, capture_output=True)
        if expected_stdout != result.stdout:
            print("Failed")
            print(f"\tCommand: {command}")
            print(f"\tExpected: {expected_stdout}")
            print(f"\tActual: {result.stdout}")

        count += 1
    print(f"Ran {count} tests")

    os.chdir(cwd)


main()
