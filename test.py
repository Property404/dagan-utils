#!/usr/bin/env python3
"""Run test cases for dagan-utils"""

import json
import os
import subprocess
import sys
import tempfile
import time


def fail(reason, command, info, result):
    """Indicate a test case failed"""
    print("Test failed")
    print(f"\tReason: {reason}")
    for key, value in info.items():
        print(f"\t{key}: {value}")

    print(f"\tCommand: {command}")
    print(f"\tStdout: {result.stdout}")
    print(f"\tStderr: {result.stderr}")
    print(f"\tStatus: {result.returncode}")
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
        expected_stdout = bytes(test_case["stdout"], "ascii")
        if expected_stdout != result.stdout:
            fail(
                "Unexpected stdout",
                command,
                {
                    "Expected stdout": expected_stdout,
                },
                result,
            )
    if "stderr" in test_case:
        expected_stderr = bytes(test_case["stderr"], "ascii")
        if expected_stderr != result.stderr:
            fail(
                "Unexpected stderr",
                command,
                {
                    "Expected stderr": expected_stderr,
                },
                result,
            )

    if "exit" in test_case:
        expected_exit_status = int(test_case["exit"])
    else:
        expected_exit_status = 0

    if expected_exit_status != result.returncode:
        fail(
            "Unexpected exit status",
            command,
            {
                "Expected status": expected_exit_status,
            },
            result,
        )

    if "max_time" in test_case:
        max_time = test_case["max_time"]
    else:
        max_time = 1

    if elapsed_time > max_time:
        fail(
            "Took too long",
            command,
            {
                "Elapsed time": f"{elapsed_time}s",
                "Max elapsed time": f"{max_time}s",
            },
            result,
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

        for file in os.listdir(tempdir):
            os.unlink(file)
        os.chdir(cwd)
        os.rmdir(tempdir)

        count += 1

    print(f"Ran {count} tests")


main()
