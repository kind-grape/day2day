import os 
import ast 
import hvac
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = hvac.Client(
    url='https://vault-tst.npe-services.t-mobile.com/',
    #url='https://vault-dev.npe-services.t-mobile.com/',
    token=os.environ.get('VAULT_TOKEN'),
    #namespace='pcf',
    verify=False, # In case you want to run without validating certs 
)

def GetAuthAccessor (authMethod):
    # returned response is a dict object
    if '/' not in authMethod:
        authMethod += '/'
    auth_methods = client.sys.list_auth_methods()
    #print('The following auth methods are enabled: {auth_methods_list}'.format(auth_methods_list=', '.join(auth_methods['data'].keys()),))
    #print(json.dumps(auth_methods, indent=1))
    authAccessor = auth_methods[authMethod]['accessor']
    return authAccessor
    
def updateAlias (aliasID, entID, name, mountAccessor):
    client.secrets.identity.update_entity_alias(
        alias_id=aliasID,
        name=name,
        canonical_id=entID,
        mount_accessor=mountAccessor,
    )
    print ('Alias '+ aliasID + ' has been updated')

    

newAuth = "okt"
newAuthAcs = GetAuthAccessor (newAuth)

with open('oidcAliasID.log', 'r') as f:
    oidcAliasID = ast.literal_eval(f.read())

with open('oidcEntID.log', 'r') as f:
    oidcEntID = ast.literal_eval(f.read())

with open('oidcAliasName.log', 'r') as f:
    oidcAliasName = ast.literal_eval(f.read())

with open('oktAliasID.log', 'r') as f:
    oktAliasID = ast.literal_eval(f.read())

with open('oktEntID.log', 'r') as f:
    oktEntID = ast.literal_eval(f.read())

with open('oidcAliasName.log', 'r') as f:
    oktAliasName = ast.literal_eval(f.read())

print("now we have the list of IDs as python var")

print("now update the list okt alias IDs")

def updateAllOktAlias ():
    pos = 0
    for i in oktAliasID:
      updateAlias(i, oktEntID[pos],oktAliasName[pos],newAuthAcs)
      pos += 1

updateAllOktAlias()


