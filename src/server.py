from flask import Flask, jsonify
from passthrough_handler import *
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from decouple import config
import requests 
import base64
import json



ORGANIZATION = ['https://tfs.eprod.com/LS']

TFS_SELECTED_PROJECTS = ['Estream'] 

PIPELINE_IDS = { "Firebird K8s Deploy" : 1044 }

ORG_URL = ORGANIZATION[0]

payload = {
    "templateParameters" : {"environment" : "drizzy-214345",
                            "passthrough" : "Hello World"}}

class TFSProject:
    def __init__(self,name: str, id: str):
        self.name = name
        self.id = id


app = Flask(__name__)


def connect_to_azure_devops(person_access_token: str, org_url: str) -> Connection:
    organization_url = org_url
    
    # Create a connection to the org
    credentials = BasicAuthentication('', person_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    return connection
# Use Version 6 for Azure REST Endpoints
def make_request_to_azure_devops(personal_access_token: str, azure_url: str) -> requests:
    pat = personal_access_token
    authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
    headers = {'Accept' : 'application/json', 'Authorization' : 'Basic '+authorization}
    res = requests.get(url=azure_url,
                headers=headers)
    
    return res

def post_params_to_firebird_k8s_deploy(personal_access_token: str, azure_url: str,body: str):
    pat = personal_access_token
    authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')
    headers = {'Accept' : 'application/json','Content-type' : 'application/json', 'Authorization' : 'Basic '+authorization}
    res = requests.post(url=azure_url,
                headers=headers,
                data=body)
    
    return res.status_code


@app.route('/', methods=['GET'])
def service_page():
    return jsonify({"message": "service"})


@app.route('/deploy', methods=['GET'])
def pass_to_firebird_k8s_deploy():
    personal_access_token = config('ACCESS_TOKEN')

    conn = connect_to_azure_devops(person_access_token=personal_access_token,
                                org_url=ORG_URL)
    
    core_client = conn.clients.get_core_client()

    get_projects_response =  core_client.get_projects()

    tfs_projects = []
    for project in get_projects_response:
        if project.name in TFS_SELECTED_PROJECTS:
            tfs = TFSProject(name=project.name,
                                    id=project.id)
            tfs_projects.append(tfs)
    


    deployment_res = post_params_to_firebird_k8s_deploy(personal_access_token=personal_access_token,
                                                        azure_url=f'{ORG_URL}/{tfs_projects[0].name}/_apis/pipelines/{PIPELINE_IDS["Firebird K8s Deploy"]}/runs?api-version=6.1-preview.1',
                                                        body=json.dumps(payload))

    return jsonify({"message" : deployment_res})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')