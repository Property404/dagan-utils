#!/usr/bin/env bash
# Lint files in this repository

# Launch an array of actions in the background and wait for them
do_lints() {
	declare -n methods="$1"
	# Keep a list of flags to detect which job failed/passed
	declare -a flags;

	for method in "${methods[@]}"; do
		echo "$method"
		# Run lint job and raise flag on failure
		flag_name="/tmp/linter_err_flag_$((RANDOM))"
		flags+=("$flag_name")
		pee "chronic $method || touch $flag_name"&
	done

	for method in "${methods[@]}"; do
		wait
	done

	# Fail if any of our jobs failed
	for flag in "${flags[@]}"; do
		if [ -f "$flag" ];then
			echo "Linting failed"
			rm "$flag"
			exit 1
		fi
	done
}

main() {
	declare -a python_files;
	declare -a shell_files;

	# Locate all files that need to be linted
	for f in ./bin/*; do
		# Python files
		if head -n 1 "$f" | chronic grep 'python'; then
			python_files+=("$f")

		# Shell files
		elif head -n 1 "$f" | chronic grep 'sh$'; then
			shell_files+=("$f")
		else
			echo "Can't lint unknown file type: $f"
			exit 1
		fi
	done

	# Lint self, too
	shell_files+=("$0")

	# Shellcheck thinks this is unused
	# shellcheck disable=SC2034
	lints=(
	"parallel shellcheck --color=always ::: ${shell_files[*]}"
	"parallel black --check ::: ${python_files[*]}"
	"parallel pylint ::: ${python_files[*]}"
	)
	do_lints lints
}

main
