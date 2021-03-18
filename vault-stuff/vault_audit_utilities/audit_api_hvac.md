## use hvac library in python prerequisite
1. make sure python3 is installed
2. navigate to the folder desired
3. create an virtual env 
    virtualenv -p 'python executable path' hvac
4. source hvac/bin/activate
5. install hvac
    pip install hvac
6. interact with vault in python env
python
>>> import hvac
>>> import os
>>> 
client = hvac.Client(
    url='https://vault-dev.npe-services.t-mobile.com',
    token=os.environ.get('VAULT_TOKEN'),
    namespace='pcf',
    verify=False, # In case you want to run without validating certs 
)



## getting the list of group names -> output group name list
api_mothod:
curl -k --header "X-Vault-Token: $VAULT_TOKEN" --request LIST https://vault-dev.npe-services.t-mobile.com/v1/identity/group/name | jq .data.keys

hvac method:
list_response = client.secrets.identity.list_groups_by_name()
group_keys = list_response['data']['keys']
print('The following group names are currently present: {keys}'.format(keys=group_keys))



## read group info by name, get its policies
api_method:
curl -k --header "X-Vault-Token: $VAULT_TOKEN" https://vault-dev.npe-services.t-mobile.com/v1/pcf/identity/group/name/PE_GENERAL_ADMINS | jq .data.policies

hvac_method:
lookup_response = client.secrets.identity.lookup_group(
        name='PE_GENERAL_ADMINS',
)
group_policy = lookup_response['data']['policies']
print('policies for "PE_GENERAL_ADMINS" is: {policy}'.format(policy=group_policy))



## for each of the policies, list all the ACL content
api_method:
curl -k --header "X-Vault-Token: $VAULT_TOKEN" https://vault-dev.npe-services.t-mobile.com/v1/sys/policies/acl/pcf_ns_admin | jq .data.policy

hvac_method:
hvac_policy_rules = client.sys.read_policy(name='pcf_ns_admin')['data']['rules']
print('pcf_ns_admin policy rules:\n%s' % hvac_policy_rules)


## list all the secret where platform engineering team owns
### kv v1
api_method:
curl -k --header "X-Vault-Token: $VAULT_TOKEN" --request LIST https://vault-dev.npe-services.t-mobile.com/v1/pcf/secret/pe

hvac_method:
list_secrets_result = client.secrets.kv.v1.list_secrets(mount_point='pe',path='ci')
print('The following paths are available under "pe" prefix: {keys}'.format(
    keys=','.join(list_secrets_result['data']['keys']),
))

### kv v2
api_method:
curl -k --header "X-Vault-Token: $VAULT_TOKEN" --request LIST https://vault-dev.npe-services.t-mobile.com/v1/tmobile/metadata | jq .data.keys

hvac method:
list_response = client.secrets.kv.v2.list_secrets(
    mount_point='pcf-test-kv',
    path='',
)
print('The following paths are available under "pcf-test-kv" prefix: {keys}'.format(
    keys=','.join(list_response['data']['keys']),
))
