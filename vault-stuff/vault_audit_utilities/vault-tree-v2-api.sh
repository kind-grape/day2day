#!/usr/bin/env bash
# usage bash vault-tree-v2.sh


function walk() {

  for secret in $(curl -s -k --header "X-Vault-Token: $VAULT_TOKEN" --request LIST https://vault-dev.npe-services.t-mobile.com/v1/tmobile/metadata$1 | jq  .data.keys |  jq -r -c '.[]'| sed  's/- //g') 
  do
    if [[ ${secret} == *"/" ]] ; then
      walk "${1}/${secret%/}"
    else
      echo "tmobile${1}/${secret}"
    fi
  done
}

query="${1}"

echo "${1}"
walk ${query}