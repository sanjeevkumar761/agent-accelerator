# Import the needed credential and management objects from the libraries.
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.workloadssapvirtualinstance import WorkloadsSapVirtualInstanceMgmtClient
import os
from dotenv import load_dotenv
import json
from func_ai.utils.llm_tools import OpenAIInterface
from func_ai.utils.openapi_function_parser import OpenAPISpecOpenAIWrapper

load_dotenv()

def getAzureResourceGroups():

    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    print(subscription_id)

    # Acquire a credential object.
    credential = DefaultAzureCredential()


    # Obtain the management object for resources.
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Retrieve the list of resource groups
    group_list = resource_client.resource_groups.list()

    #print(json.dumps(group_list))

    # Show the groups in formatted output
    #column_width = 40

    #print("Resource Group".ljust(column_width) + "Location")
    #print("-" * (column_width * 2))

    #strRG = ""
    #for group in list(group_list):
    #    print(f"{group.name:<{column_width}}{group.location}")

    #for group in list(group_list):
    #    strRG = strRG + (f"{group.name:<{column_width}}{group.location}")
    data=[]
    for group in list(group_list):
        item = {"groupName": group.name, "location": group.location}
        data.append(item)

    jsonData=json.dumps(data)
    #print(jsonData)

    return jsonData

def getResourceyByAzureResourceGroup(rgName):
    load_dotenv()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    print(subscription_id)

    # Acquire a credential object.
    credential = DefaultAzureCredential()


    # Obtain the management object for resources.
    resource_client = ResourceManagementClient(credential, subscription_id)

    resource_list = resource_client.resources.list_by_resource_group(
       rgName, expand = "createdTime,changedTime")

    # Show the groups in formatted output
    column_width = 36

    #print("Resource".ljust(column_width) + "Type".ljust(column_width)
    #    + "Create date".ljust(column_width) + "Change date".ljust(column_width))
    #print("-" * (column_width * 4))

    #for resource in list(resource_list):
    #    print(f"{resource.name:<{column_width}}{resource.type:<{column_width}}"
    #    f"{str(resource.created_time):<{column_width}}{str(resource.changed_time):<{column_width}}")

    data=[]
    for resource in list(resource_list):
        item = {"resourceName": resource.name, "resourceType": resource.type}
        data.append(item)

    #jsonData=json.dumps(data)

    return data

def getSAPVISList():
    load_dotenv()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    print(subscription_id)

    # Acquire a credential object.
    credential = DefaultAzureCredential()

    client = WorkloadsSapVirtualInstanceMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
    )

    vislist = client.sap_virtual_instances.list_by_subscription()


    #print(vis.properties)
    #for item in response:
    #        print(item)

    data=[]
    for vis in list(vislist):
        #print(vis)
        item = {"visid": vis.id, "visname": vis.name}
        data.append(item)

    jsonData=json.dumps(data)
    #print(jsonData)

    return jsonData

def getSAPVIS(rgName, visName):
    load_dotenv()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    print(subscription_id)

    # Acquire a credential object.
    credential = DefaultAzureCredential()

    client = WorkloadsSapVirtualInstanceMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
    )

    vis = client.sap_virtual_instances.get(
        resource_group_name=rgName,
        sap_virtual_instance_name=visName,
    )

    item = {"visid": vis.id, "visname": vis.name, "visproduct": vis.properties.environment, "visstatus": vis.properties.status, "vislocation": vis.location, "visprovisioningState": vis.properties.provisioning_state}
    jsonData=json.dumps(item)
    print(jsonData)

    return jsonData

def getSAPVISAppServer(rgName, visName, appServerInstanceName):
    load_dotenv()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    print(subscription_id)

    # Acquire a credential object.
    credential = DefaultAzureCredential()

    client = WorkloadsSapVirtualInstanceMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
    )

    #vislist = client.sap_virtual_instances.list_by_subscription()
    appserver = client.sap_application_server_instances.get(
        resource_group_name=rgName,
        sap_virtual_instance_name=visName,
        application_instance_name=appServerInstanceName
    )

    #print(vis.properties)
    #for item in response:
    #        print(item)

    #data=[]
    #for vis in list(vis):
        #print(vis)
    #    item = {"visid": vis.id, "visname": vis.name}
    #    data.append(item)

    item = {"appserverid": appserver.id, "appservername": appserver.name, "appserverkernelPatch": appserver.properties.kernel_patch, "appserverkernelVersion": appserver.properties.kernel_version}
    jsonData=json.dumps(item)
    print(jsonData)

    return jsonData

def stopSAPVISInstance(rgName, visName, appServerName):
    load_dotenv()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    print(subscription_id)

    # Acquire a credential object.
    credential = DefaultAzureCredential()

    client = WorkloadsSapVirtualInstanceMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
    )

    # Stop the SAP Virtual Instance
    client.sap_application_server_instances.begin_stop_instance(
        resource_group_name=rgName,
        sap_virtual_instance_name=visName,
        application_instance_name=appServerName,
    )

    print(f"SAP Virtual Instance {visName} in resource group {rgName} has been stopped.")

    return f"SAP Virtual Instance {visName} in resource group {rgName} has been stopped."

def main():

    # Let the assistant start the conversation.  It will end when the user types exit.
    getAzureResourceGroups()


if __name__ == "__main__":
    main()