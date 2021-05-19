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
    

newAuth = "aad"
newAuthAcs = GetAuthAccessor (newAuth)

with open('oidcAliasID.log', 'r') as f:
    oidcAliasID = ast.literal_eval(f.read())

with open('oidcEntID.log', 'r') as f:
    oidcEntID = ast.literal_eval(f.read())

with open('oktAliasID.log', 'r') as f:
    oktAliasID = ast.literal_eval(f.read())

with open('oktEntID.log', 'r') as f:
    oktAEntID = ast.literal_eval(f.read())

print("now we have the list of IDs as python var")

print("now update the list okt alias IDs")
