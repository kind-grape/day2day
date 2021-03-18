import hvac
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = hvac.Client(
    url='https://vault-dev.npe-services.t-mobile.com',
    token=os.environ.get('VAULT_TOKEN'),
    #namespace='pcf',
    verify=False, # In case you want to run without validating certs 
)

def recursive_lookup(mount,kv_path):
    if '/' not in kv_path and kv_path:
        kv_path=kv_path+'/'
    list_response = client.secrets.kv.v2.list_secrets(mount_point=mount, path=kv_path,)
    #print (list_response['data']['keys'])
    for i in list_response['data']['keys']:
        if '/' in i:
            #print ('loopagain ' + kv_path + i)
            recursive_lookup(mount,kv_path + i)
        else:
            #print('The following paths are available under "tmobile/" prefix: {keys}'.format(keys=','.join(list_response['data']['keys'][]),))
            print (mount+'/'+kv_path+i )

recursive_lookup('tmobile','')
