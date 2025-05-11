#!/usr/bin/env bash
_peval() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"
    local opts

    if [[ "${cur}" =~ "-" ]]; then 
        opts="-h --help -x --hexadecimal -b --binary -o --octal -n --no-newline"
    fi

    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
}

complete -F _peval peval
