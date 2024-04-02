from autogen import UserProxyAgent, ConversableAgent, config_list_from_json
from typing_extensions import Annotated, Literal
import autogen
import requests
import xmltodict, json
from azure_arg import getAzureResourceGroups, getResourceyByAzureResourceGroup, getSAPVISList, getSAPVIS, getSAPVISAppServer, stopSAPVISInstance
from json2table import convert
import asyncio
from user_proxy_webagent import UserProxyWebAgent

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample.
# For example, if you have created a OAI_CONFIG_LIST file in the current working directory, that file will be used.
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
gpt35_config = {"config_list": config_list, "temperature":0, "seed": 53}

llm_config_assistant = {
    "model":"gpt-4",
    "temperature": 0,
    "config_list": config_list,
        "functions": [
        {
            "name": "getazurerg",
            "description": "List Azure Resource Groups"
        },
        {
            "name": "getsapvislist",
            "description": "List SAP systems"
        },
        {
            "name": "getsapvis",
            "description": "Get SAP system details",
            "parameters": {
                "type": "object",
                "properties": {
                    "rgName": {
                        "type": "string",
                        "description": "Resource Group Name",
                    },
                    "visName": {
                        "type": "string",
                        "description": "VIS Name",
                    }
                }
            }
        },
        {
            "name": "getsapvisappserver",
            "description": "Get SAP app server instance details",
            "parameters": {
                "type": "object",
                "properties": {
                    "rgName": {
                        "type": "string",
                        "description": "Resource Group Name",
                    },
                    "visName": {
                        "type": "string",
                        "description": "VIS Name",
                    },
                    "appServerName": {
                        "type": "string",
                        "description": "App Server Name",
                    }
                }
            }
        }, 
        {
            "name": "stopsapvisinstance",
            "description": "Stop SAP app server instance details",
            "parameters": {
                "type": "object",
                "properties": {
                    "rgName": {
                        "type": "string",
                        "description": "Resource Group Name",
                    },
                    "visName": {
                        "type": "string",
                        "description": "VIS Name",
                    },
                    "appServerName": {
                        "type": "string",
                        "description": "App Server Name",
                    }
                }
            }
        }
    ],
}

input_future = None



class AutogenChat():
    def __init__(self, chat_id=None, websocket=None):
        self.websocket = websocket
        self.chat_id = chat_id
        self.client_sent_queue = asyncio.Queue()
        self.client_receive_queue = asyncio.Queue()

        self.assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config=llm_config_assistant,
            system_message="""You are a helpful assistant."""
        )

        self.user_proxy = UserProxyWebAgent(  
            name="user_proxy",
            human_input_mode="ALWAYS", 
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
            function_map={
                "getazurerg": self.getazurerg,
                "getsapvislist": self.getsapvislist,
                "getsapvis": self.getsapvis,
                "getsapvisappserver": self.getsapvisappserver,
                "stopsapvisinstance": self.stopsapvisinstance
            }
        )

        # add the queues to communicate 
        self.user_proxy.set_queues(self.client_sent_queue, self.client_receive_queue)

    async def start(self, message):
        await self.user_proxy.a_initiate_chat(
            self.assistant,
            #clear_history=True,
            clear_history=False,
            message=message
        )

    def getazurerg(anything) -> list:
        rgs = getAzureResourceGroups()
        return rgs
    
    def getsapvislist(anything) -> list:
        print("DEBUG ...1")
        sapvislist = getSAPVISList()
        print("DEBUG ...2")
        print(sapvislist)
        return sapvislist
    
    def getsapvis(self, rgName=None, visName=None) -> list:
        print("DEBUG ...1")
        sapvis = getSAPVIS(rgName, visName)
        print("DEBUG ...2")
        print(sapvis)
        return sapvis
    def getsapvisappserver(self, rgName=None, visName=None, appServerName=None) -> list:
        print("DEBUG ...1")
        appserver = getSAPVISAppServer(rgName, visName, appServerName)
        print("DEBUG ...2")
        print(appserver)
        return appserver
    
    def stopsapvisinstance(self, rgName=None, visName=None, appServerName=None) -> list:
        print("DEBUG ...1")
        statusMessage = stopSAPVISInstance(rgName, visName, appServerName)
        print("DEBUG ...2")
        print(statusMessage)
        return statusMessage


#autogen.agentchat.register_function(
#    getazurerg,
#    caller=assistant,
#    executor=user_proxy,
#    name="rg",
#    description="get azure resource groups",
#)


#def main():
    # Let the assistant start the conversation.  It will end when the user types exit.
#    assistant.initiate_chat(user_proxy, message="How can I help you today?")


#if __name__ == "__main__":
#    main()

