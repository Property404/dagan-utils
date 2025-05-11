#!/usr/bin/env bash
_kvs() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"
    local opts="store get snip rm list -h --help -d --database"

    case "${prev}" in
        get|store|snip|rm) opts="$(kvs list | cut -d' ' -f1)"
    esac

    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
}

complete -F _kvs kvs
