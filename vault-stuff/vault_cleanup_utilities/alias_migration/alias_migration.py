# this script is used to create a list of alias needed to mass update the auth accessor field once new OIDC auth method has been mounted

import hvac
import urllib3
import os
import json
# what kind of entities we want to clean up?
# 
# entity_abb56xh types random entity names that are created by vault with some legit entity alias from a mount
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = hvac.Client(
    url='https://vault-tst.npe-services.t-mobile.com/',
    #url='https://vault-dev.npe-services.t-mobile.com/',
    token=os.environ.get('VAULT_TOKEN'),
    #namespace='pcf',
    verify=False, # In case you want to run without validating certs 
)

# get auth accessor value for particular auth method 
def GetAuthAccessor (authMethod):
  # returned response is a dict object
    if '/' not in authMethod:
        authMethod += '/'
    auth_methods = client.sys.list_auth_methods()
    #print('The following auth methods are enabled: {auth_methods_list}'.format(auth_methods_list=', '.join(auth_methods['data'].keys()),))
    #print(json.dumps(auth_methods, indent=1))
    authAccessor = auth_methods[authMethod]['accessor']
    return authAccessor

def get_alias_list ():
    list_response = client.secrets.identity.list_entity_aliases()
    alias_keys = list_response['data']['keys']
    return alias_keys

# check how many alias out there
allAlias = get_alias_list()
#print (len(allAlias))


# readAliasRes = client.secrets.identity.read_entity_alias(
#         alias_id="e0d22527-8819-ff51-2726-865dee4a6fba",
# )
# print (readAliasRes)
# {'request_id': 'd1e80c32-4b19-53b0-eb06-4190df4a2322', 'lease_id': '', 'renewable': False, 'lease_duration': 0, 'data': {'canonical_id': '8d481e48-7355-1da6-2c32-5019fe33a1bb', 'creation_time': '2021-04-29T15:42:40.504736407Z', 'id': 'fef2ddad-2960-5d58-69a8-a8570c962b3f', 'last_update_time': '2021-04-29T15:42:40.504736407Z', 'merged_from_canonical_ids': None, 'metadata': None, 'mount_accessor': 'auth_oidc_beb2c3a1', 'mount_path': 'auth/okt/', 'mount_type': 'oidc', 'name': 'Venkatasubbarao.Pothuri2@T-Mobile.com', 'namespace_id': 'root'}, 'wrap_info': None, 'warnings': None, 'auth': None}


oktAliasFile = open("oktAliasID.log", "w")
oktEntFile = open("oktEntID.log", "w")

oidcAliasFile = open("oidcAliasID.log", "w")
oidcEntFile = open("oidcEntID.log", "w")

def get_okt_alias (aliasArr):
    okt_accessor = GetAuthAccessor('okt')
    oktAliasID = []
    oktEntID = []

    aad_accessor = GetAuthAccessor('oidc')
    oidcAliasID = []
    oidcEntID = []

    for aliasID in aliasArr:
        readAliasID  = client.secrets.identity.read_entity_alias(alias_id=aliasID,)
        if readAliasID['data']['mount_accessor'] == okt_accessor:
            oktAliasID.append(aliasID)
            oktEntID.append(readAliasID['data']['canonical_id'])
        elif readAliasID['data']['mount_accessor'] == aad_accessor:
            oidcAliasID.append(aliasID)
            oidcEntID.append(readAliasID['data']['canonical_id'])
    
    print (len(oktAliasID))
    oktAliasFile.write(str(oktAliasID))
    oktAliasFile.close()

    print (len(oktEntID))
    oktEntFile.write(str(oktEntID))
    oktEntFile.close()

    print (len(oidcAliasID))
    oidcAliasFile.write(str(oidcAliasID))
    oidcAliasFile.close()

    print (len(oidcEntID))
    oidcEntFile.write(str(oidcEntID))
    oidcEntFile.close()
    #return oktAliasID

get_okt_alias(allAlias)

         








