#!/usr/bin/env bash

main() {
    local -r test_cases="tests/cases.json"

    if [[ -n "${1}" ]]; then
        echo "Unexpected argument: ${1}" >&2
        return 1
    fi

    PATH="${PATH}:./bin/"

    local cmd
    local expected
    local actual
    for (( i=0; ; i++ )); do
        jq -e ".[$i]" "${test_cases}" > /dev/null || break
        cmd="$(jq -re ".[$i].run" "${test_cases}")"
        actual="$(bash -c "${cmd}")"
        expected="$(jq -re ".[$i].output" "${test_cases}")"
        if [[ "${expected}" != "${actual}" ]]; then
            echo "Failed:"
            echo -e "\tCommand: ${cmd}"
            echo -e "\tExpected: ${expected}"
            echo -e "\tActual: ${actual}"
            return 1;
        fi
    done
    echo "Ran $i tests"
}

main "${@}"
