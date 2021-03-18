#!/usr/bin/env bash
# usage: bash vault-tree-v1 path-to-check
function walk() {
  for secret in $(vault list $1 | tail -n +3)
  do
    if [[ ${secret} == *"/" ]] ; then
      walk "${1}${secret}"
    else
      echo "${1}${secret}"
    fi
  done
}

query="${1}"

if [[ ${query} != *"/" ]] ; then
  query=${query}/
fi

echo "${1}"
walk ${query}