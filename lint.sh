#!/usr/bin/env bash
# Lint files in this repository

# Launch an array of actions in the background and wait for them
do_lints() {
	local -n methods="$1"
	# Keep a list of flags to detect which job failed/passed
	local -a flags;

	for method in "${methods[@]}"; do
		echo "$method"
		# Run lint job and raise flag on failure
		flag_name="/tmp/linter_err_flag_$((RANDOM))"
		flags+=("$flag_name")
		bash -c "$method || touch $flag_name"&
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
	local -a python_files;
	local -a shell_files;

	# Locate all files that need to be linted
	for f in ./bin/*; do
		# Python files
		if head -n 1 "$f" | grep -q 'python'; then
			python_files+=("$f")

		# Shell files
		elif head -n 1 "$f" | grep -q 'sh$'; then
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
	"shellcheck --color=always ${shell_files[*]}"
	"black --check ${python_files[*]}"
	"pylint ${python_files[*]}"
	)
	do_lints lints
}

main
