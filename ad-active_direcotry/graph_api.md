## Using Microsoft Graph API
Where AD related tasks are needed and you cant run get AD powershell for some reason, such as in Linux/Mac environment, you can use the web based graph api tool to fullfill the need. 
https://developer.microsoft.com/en-us/graph/graph-explorer 

## Some useful queries I have run
### users
Get my profile 
```
GET https://graph.microsoft.com/v1.0/me 
```

Search the user ID by providing the "userPrincipalName"/UPN - this could be email addr or the user login ID
```
GET https://graph.microsoft.com/v1.0/users?$filter=startswith(userPrincipalName,'<user_display_name>')&$select=displayName,id
```

### groups
get a particular user's direct group membership by providing the id of the user; only return the displayName and the ID fields
```
GET https://graph.microsoft.com/v1.0/users/<user_id>/memberOf/microsoft.graph.group?$select=displayName,id
```
request body - this ensures only the direct member will return
```
{
    "securityEnabledOnly": true
}
```

Search a particular group with all the attributes by providing the 'displayName' - group name most of the time 
```
GET https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName, '<group name>')&$count=true
```




