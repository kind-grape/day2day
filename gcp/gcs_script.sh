#!/bin/bash
echo "Loading Audience From GCP WIF Cred"
#credential_location=/var/run/secrets/google/credentials_config.json"
credential_location="credential_config.json"
audience=$(cat $credential_location | jq -r .audience)
echo $audience
echo "Loading Token from K8S SA"
#token_location=$(cat $credential_location | jq -r .credential_source.file)
token_location="token"
token=$(cat $token_location)
echo $token

## Other Variables such as GCS project/bucket should be load from ENV VAR


echo "Construct the GCP Payload for OAuth Token Excahnge"
#payload_location=""
payload_location="payload.json"
#jq ".audience = \"$audience\"" $payload_location > $payload_location
jq -M ". + {audience:\"$audience\", subject_token:\"$token\"}" $payload_location > $payload_location.tmp && mv $payload_location.tmp $payload_location
cat $payload_location

echo "POST to google STS endpoint to get OAuth Token"
oauth_token=$(curl --request POST -H "Content-Type: application/json" -d @$payload_location https://sts.googleapis.com/v1/token | jq -r .access_token)
cat oauth_token

echo "Running GCS API to upload snapshot to bucket"
# the following ENV VAR should exist
# $object_path: location for snapshot 
# $bucket_name: GCS bucket 
# $snapshot_dir: sub folder inside bucket

curl -X POST --data-binary @$object_path -H "Authorization: Bearer $oauth_token" -H "Content-Type: application/x-gzip" "https://storage.googleapis.com/upload/storage/v1/b/$bucket_name/o?uploadType=media&name=$snapshot_dir/$obj_name"
