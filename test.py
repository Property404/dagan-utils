#!/usr/bin/env python3
"""Run test cases for dagan-utils"""

import json
import os
import subprocess
import sys
import tempfile
import time


def fail(info):
    """Indicate a test case failed"""
    print("Test failed")
    for (key, value) in info.items():
        print(f"\t{key}: {value}")
    sys.exit(1)


def run_test_case(test_case):
    """Run a single test case"""
    command = test_case["run"]
    commands = ["bash", "-c", command]

    start_time = time.time()
    try:
        result = subprocess.run(commands, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        result = exc
    except Exception as exception:
        raise exception
    elapsed_time = time.time() - start_time

    if "stdout" in test_case:
        expected_stdout = bytes(test_case["stdout"] + "\n", "ascii")
        if expected_stdout != result.stdout:
            fail(
                {
                    "Command": command,
                    "Expected": expected_stdout,
                    "Actual": result.stdout,
                }
            )

    if "exit" in test_case:
        expected_exit_status = int(test_case["exit"])
    else:
        expected_exit_status = 0

    if expected_exit_status != result.returncode:
        fail(
            {
                "Command": command,
                "Expected status": expected_exit_status,
                "Actual status": result.returncode,
            }
        )

    if "max_time" in test_case:
        max_time = test_case["max_time"]
    else:
        max_time = 1

    if elapsed_time > max_time:
        fail(
            {
                "Command": command,
                "Elapsed time": f"{elapsed_time}s",
                "Max elapsed time": f"{max_time}s",
            }
        )


def main():
    """Main function"""

    with open("tests/cases.json", encoding="utf-8") as file:
        tests = json.loads(file.read())

    cwd = os.getcwd()
    os.environ["PATH"] = f"{cwd}/bin/:{os.environ['PATH']}"

    count = 0
    for test in tests:
        tempdir = tempfile.mkdtemp()
        os.chdir(tempdir)

        files = []
        if "files" in test:
            files = test["files"]
            for filename in files:
                with open(filename, "wb") as file:
                    contents = files[filename]
                    file.write(bytes(contents.encode("ascii")))

        if "cases" in test:
            for case in test["cases"]:
                run_test_case(case)
        else:
            run_test_case(test)

        for file in files:
            os.unlink(file)
        os.chdir(cwd)
        os.rmdir(tempdir)

        count += 1

    print(f"Ran {count} tests")


main()
