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

# return all entity name list 
def GetAllEntityNames ():
    list_response = client.secrets.identity.list_entities_by_name()
    entity_names = list_response['data']['keys']
    return entity_names

# return all entity names that are not standard naming standard
def FilterNonStandardEntityNames (entityNameArr):
    NSEntArr = []
    for i in entityNameArr:
        if 'entity_' not in i:
            NSEntArr.append(i)
        if 'entity_' in i and '@T-Mobile.com' not in i.split("entity_",1)[1]:
            NSEntArr.append(i)
    return NSEntArr

def ReadEntityAliases(entityName):
    read_response = client.secrets.identity.read_entity_by_name(name=entityName,)
    entityAliases = read_response['data']['aliases']
    return entityAliases

# get list of entities without alias
def GetEntitiesWithoutAliases(entityNameArr):
    emptyAliasEntArr = []
    for i in entityNameArr:
        if not ReadEntityAliases(i):
            emptyAliasEntArr.append(i)
    return emptyAliasEntArr

# get list of entities with aliases
def GetEntitiesWithAliases (entityNameArr):
    AliasEntArr = []
    for i in entityNameArr:
        if ReadEntityAliases(i):
             AliasEntArr.append(i)
    return AliasEntArr

def PrintEntitiesWithoutAliases ():
    emptyAliasEntArr = GetEntitiesWithoutAliases(FilterRandomEntityNames(GetAllEntityNames()))
    print( 'Following entities have no aliases and should be removed ' + str(emptyAliasEntArr) )

def DeleteEntityNames (entityNameArr):
    for i in entityNameArr:
        client.secrets.identity.delete_entity_by_name(name=i,)
    print('entities have been removed based on the input entity names')

# this is to get the list of entities with only alias that are from ldap auth method
def GetEntitiesWithLDAP (entityNameArr):
    entities = []
    for i in entityNameArr:
        # now read the aliasses list for each entities
        auth_count = 0
        if len(ReadEntityAliases(i)) is 1 and ReadEntityAliases(i)[0]['mount_accessor'] == GetAuthAccessor('ldap'):
            auth_count += 1
        if auth_count is 1:
            entities.append(i)

        # for r in ReadEntityAliases(i):
        #     if r['mount_accessor'] == GetAuthAccessor('ldap'):
        #         # if there was a matching auth accessor this count should increase
        #         auth_count += 1
        # if auth_count is 1:
        #     entities.append(i)
    print ('following entities have ONLY ldap auth method alias ' + str(entities))
    return entities

# this is to get the list of entities with aliases that are from cdp(jwt) auth method
def GetEntitiesWithCDP (entityNameArr):
    entities = []
    for i in entityNameArr:
        # now read the aliasses list for each entities
        auth_count = 0
        for r in ReadEntityAliases(i):
            if r['mount_accessor'] == GetAuthAccessor('cdp'):
                # if there was a matching auth accessor this count should increase
                auth_count += 1
        if auth_count is 1:
            entities.append(i)
    print ('following entities have cdp auth method alias ' + str(entities))
    return entities

# this is to get the list of entities with aliases that are from AAD(oidc) auth method
def GetEntitiesWithAAD (entityNameArr):
    entities = []
    for i in entityNameArr:
        # now read the aliasses list for each entities
        auth_count = 0
        for r in ReadEntityAliases(i):
            if r['mount_accessor'] == GetAuthAccessor('oidc'):
                # if there was a matching auth accessor this count should increase
                auth_count += 1
        if auth_count is 1:
            entities.append(i)
    print ('following entities have AAD(oidc) auth method alias ' + str(entities))
    return entities

# this is to update the entity naming convention and consolidate entity aliasses
def ConsolidateOIDCEnt (entityNameArr):
    # update the entities for each of the entity name list 
    errorEntIDList = []
    for ent in entityNameArr:
        # first step, create the jwt auth aliase to the entity
        entID = client.secrets.identity.read_entity_by_name(name=ent,)['data']['id']
        # second step, get the user email from oidc (AAD) alias
        aliasArr = (ReadEntityAliases(ent))
        jwtEmail = ''
        for alias in aliasArr:
            if alias['mount_accessor'] == GetAuthAccessor('oidc'):
                jwtEmail = alias['name']
        # third step, add jwt auth alias 
        create_response = client.secrets.identity.create_or_update_entity_alias(name=jwtEmail, canonical_id=entID, mount_accessor=GetAuthAccessor('cdp'),)
        alias_id = create_response['data']['id']
        print('cdp auth Alias ID for ' + jwtEmail + ' is: {id}'.format(id=alias_id)) 
        # add okt auth alias
        create_response = client.secrets.identity.create_or_update_entity_alias(name=jwtEmail, canonical_id=entID, mount_accessor=GetAuthAccessor('okt'),)
        alias_id = create_response['data']['id']
        print('okta auth Alias ID for ' + jwtEmail + ' is: {id}'.format(id=alias_id)) 
        # last step, update the specific entity to the right naming convention
        updatedName = 'entity_' + jwtEmail
        try:
            update_action = client.secrets.identity.create_or_update_entity(entity_id=entID, name=updatedName,)
            print (update_action) # expected result should be 204 http response code 
        except:
            print ('entity '+ entID + ' was not updated successfully')
            errorEntIDList.append(entID)
        
        entity_details = client.secrets.identity.read_entity(entity_id=entID,)
        print( 'Entity ID for ' + entity_details['data']['id'] + ' has been update with name as ' + entity_details['data']['name'] )
    print ('entities name have been consolidated except the following ' + str(errorEntIDList) )



nonStandarEnt = FilterNonStandardEntityNames(GetAllEntityNames())
print (nonStandarEnt)
#GetEntitiesWithLDAP(nonStandarEnt)
#GetEntitiesWithAAD(nonStandarEnt)
ConsolidateOIDCEnt(['entity_1'])

#aliasArr = (ReadEntityAliases('entity_OBarron1'))




#print (ReadEntityAliases('entity_24eadb02')[0]['mount_accessor'])
#print ( GetEntitiesWithLDAP(['entity_snallus1','entity_wgray7']) )
#GetEntitiesWithLDAP( GetEntitiesWithoutAliases(GetAllEntityNames()) )
#print (GetEntitiesWithAliases(GetAllEntityNames()))
#entitiesWithAliasses = GetEntitiesWithAliases(GetAllEntityNames())
#print (GetAuthAccessor('cdp'))




