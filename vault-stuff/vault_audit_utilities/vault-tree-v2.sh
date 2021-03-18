#!/usr/bin/env bash
# usage bash vault-tree-v2.sh

function walk() {
  for secret in $(vault kv list --format=yaml $1|sed  's/- //g')
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