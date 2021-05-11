import os 
import ast 

with open('oidcAliasID.log', 'r') as f:
    oidcAliasID = ast.literal_eval(f.read())

print(type(oidcAliasID))