## Exchange Openshift WIF token with OAuth Token 

1. Get the GCP Credential File output, this would contain where the run time openshift token is
Note, this file would only exists if it was mounted from secrets volume mounts
```
cat /var/run/secrets/google/credentials_config.json
{
  "type": "external_account",
  "audience": "//iam.googleapis.com/projects/203964333557/locations/global/workloadIdentityPools/pd120-hhzps/providers/pd120-hhzps",
  "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
  "token_url": "https://sts.googleapis.com/v1/token",
  "credential_source": {
    "file": "/var/run/secrets/openshift/serviceaccount/token",
    "format": {
      "type": "text"
    }
  },
  "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{sa_email}:generateAccessToken"
} 
```  


1. Get the Openshift SA token 
```
cat /var/run/secrets/openshift/serviceaccount/token

ey....
```




1. Construct the payload for POST commands 
```
cat << EOF > payload.json
{
  "audience": "//iam.googleapis.com/projects/203964333557/locations/global/workloadIdentityPools/pd120-hhzps/providers/pd120-hhzps",
  "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
  "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "scope": "https://www.googleapis.com/auth/cloud-platform",
  "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
  "subject_token": "ey..."
}
EOF
```

1. Execute the following command to run against the google api sts endpoint
```
curl --request POST -H "Content-Type: application/json" -d @payload.json https://sts.googleapis.com/v1/token

{
  "access_token": "ya29.d.b0Aaekm1LEAgwo...",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",  "token_type": "Bearer",  "expires_in": 2963}
```

