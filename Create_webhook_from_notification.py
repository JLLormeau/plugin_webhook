#JLL
import json
import requests
import os
import urllib3


##################################
### Environment saas
##################################
Tenant="https://"+str(os.getenv('MyTenant'))
Token=os.getenv('MyToken')
activeGate_id=os.getenv('ActiveGateId')
endpoint=['xxxx','yyyy'] #filter on endpoint xxxx.domain.com or yyyy.domain.com

##################################
## API
##################################
APInotification='/api/config/v1/notifications'
APIextensions='/api/config/v1/extensions/custom.remote.python.webhook/instances'
APIalertingprofile='/api/config/v1/alertingProfiles'

##################################
## Others
##################################
AlertingProfileDic={}

#disable warning
urllib3.disable_warnings()

# variable changed if script is run on Windows or Linux. "\\" for Windows, "/" for Linux
head = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}


##################################
## Generic Dynatrace API
##################################

# generic function GET to call API with a given uri
def queryDynatraceAPI(uri):
    jsonContent = None
    response = requests.get(uri,headers=head,verify=False)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)


#generic function POST to call API with a given uri
def postDynatraceAPI(uri, payload):
    jsonContent = None
    response = requests.post(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
            jsonContent="success"
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function PUT to call API with a given uri
def putDynatraceAPI(uri, payload):
    jsonContent = None
    #print(uri,head,payload)
    response = requests.put(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        jsonContent="success"
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if (jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function Delete to call API with a given uri
def delDynatraceAPI(uri, payload):
    jsonContent = None
    #print(uri,head,payload)
    response = requests.delete(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        jsonContent="success"
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if (jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

   
##################################
## Get Problem ID
##################################
def getalertingprofile(TENANT, TOKEN):
    uri=TENANT+APIalertingprofile+'?pageSize=500&Api-Token='+TOKEN

    #print(uri)
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    alertes = datastore['values']
    for alerte in alertes :
        AlertingProfileDic[alerte['id']]=alerte['name']
    return()


def getnotification(TENANT, TOKEN):
    uri=TENANT+APInotification+'?pageSize=500&Api-Token='+TOKEN

    #print(uri)
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    notifications = datastore['values']
    newendpoint=False
    for notification in notifications :
        #print(notification['name'], notification['type'])
        if notification['type']=='WEBHOOK' :
            uri=TENANT+APInotification+'/'+notification['id']+'?Api-Token='+TOKEN
            datastore = queryDynatraceAPI(uri)
            if datastore['url'].replace('/','.').split('.')[2] in endpoint : 
            
                if datastore['alertingProfile'] in AlertingProfileDic:
                    createEndpoint(TENANT, TOKEN, datastore['url'], datastore['payload'], datastore['name'], AlertingProfileDic[datastore['alertingProfile']], datastore['name'])
                else:
                    print('Notifiaction', datastore['name'], ': alertingProfileId', datastore['alertingProfile'], 'has no reference' )
                newendpoint=True
                
    if not newendpoint:
        print('no Webhook endpoint on ',endpoint )


    return()


def createEndpoint(TENANT, TOKEN, WebhookUrl, CustomPayload, WebhookName, AlertingProfile, endpointName):
    uri=TENANT+APIextensions+'?Api-Token='+TOKEN
    payload={
          "id": "custom.remote.python.webhook",
          "enabled": False,
          "useGlobal": False,
          "properties": {
            "WebhookUrl": WebhookUrl,
            "CustomPayload": CustomPayload,
            "Tenant": TENANT,
            "Token": TOKEN,
            "debug": "false",
            "Test": "false",
            "WebhookName": WebhookName,
            "AlertingProfile": AlertingProfile
          },
          "activeGate": {
            "id": activeGate_id
          },
          "endpointName": endpointName
        }
    
    uri2=TENANT+APIextensions+'?pageSize=500&Api-Token='+TOKEN
    #print(uri2)
    datastore = queryDynatraceAPI(uri2)
    #print(datastore)
    extensionexist=False
    extensions = datastore['configurationsList']
    for extension in extensions :
        #print(extension)
        if extension['name']==endpointName :
            extensionexist=True

    if extensionexist :
        print('Webhook', endpointName, ': already created')
    else:
        postDynatraceAPI(uri, payload)
        print('Webhook', endpointName, ': is creating')

    return()

##################################
## Main program
##################################
print('Tenant',Tenant)
print('Token',Token)
print('activeGate_id',activeGate_id)
print('endpoint', endpoint)
print()
getalertingprofile(Tenant, Token)
getnotification(Tenant, Token)

