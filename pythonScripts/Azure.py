from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint

import os
import requests

PPAT="nhzgmzumv2eusupp3jb6q2tx3yywicv375ejknq6zxoixdcqfm4a"
OURL="https://dev.azure.com/ahmedrgb10"

credentials=BasicAuthentication('',PPAT)
connection=Connection(base_url=OURL,creds=credentials)

# coreClient=connection.clients.get_core_client()

# getProjectResponse=coreClient.get_projects()



# get_projects_response = coreClient.get_projects()
# index = 0
# while get_projects_response is not None:
#     for project in get_projects_response.value:
#         pprint.pprint("[" + str(index) + "] " + project.name)
#         index += 1
#     if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
#         # Get the next page of projects
#         get_projects_response = coreClient.get_projects(continuation_token=get_projects_response.continuation_token)
#     else:
#         # All projects have been retrieved
#         get_projects_response = None





# See link down below to generate your Private Access Token
AZURE_DEVOPS_PAT = os.getenv('nhzgmzumv2eusupp3jb6q2tx3yywicv375ejknq6zxoixdcqfm4a')
url = 'https://dev.azure.com/ahmedrgb10/_apis/wit/workitems/$task?api-version=5.1'

data = [
 {
 "op": "add",
 "path": "/fields/System.Title",
 "value": "Sample task"
 }
]

r = requests.get(url, json=data, 
    headers={'Content-Type': 'application/json-patch+json'},
    auth=('', PPAT))

print(r)