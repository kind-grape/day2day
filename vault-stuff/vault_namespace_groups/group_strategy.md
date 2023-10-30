## Namespace Group Strategy 
In order to manage the human access at the root namespace, while having the correct inherrited access permission, the correct approch should be the following 
    1. Create the human auth methods such as OIDC/Ldap at the parent namespace 
    1. Create the entity object such as group entity at the parent namespace (external entity with alias mapping to identity provider)
    1. In the child namespace, create an entity group, attach the appropriate policy within the child namespace in the entity group
    1. In the child namespace, add the entity from the parent namespace to the entity group as a member 
    