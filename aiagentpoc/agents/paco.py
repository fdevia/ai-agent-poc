
import json
import requests
from phi.agent import Agent, AgentMemory
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
import os
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.memory.db.sqlite import SqliteMemoryDb

"""
Returns a list of product dictionaries.

    This function retrieves product data from the API. Each product contains basic information about
    available items in the inventory.

    Returns:
        list: A list of dictionaries, each representing a product. Each dictionary contains the following keys:
            - "_id" (str): The unique identifier of the product in the database.
            - "codeCompany" (str): The company's internal product code.
            - "codeFacebook" (str): The Facebook catalog identifier for the product.
            - "title" (str): The name or title of the product.
            - "stock" (int): The current quantity available in inventory.
"""
def get_catalog():
    response = requests.get("https://chatbotlogisticsone-fb340de3b466.herokuapp.com/api/products/get-products").json()
    return json.dumps(response)

"""
This tool allows you to make a purchase.

The payload must have the following structure:

{
    "user_id": "573004654173",
    "items": [
        {
            "codeCompany": "005122",
            "quantity": 2
        }
    ]
}

Arguments:
    payload (dict): A dictionary with the keys:
        - user_id (str): The ID of the user making the purchase.
        - items (list): A list of items, each with:
            - codeCompany (str): The company's internal product code that can be found in the product catalog property called codeCompany
            - quantity (int): The quantity to purchase.
"""
def create_purchase(payload):
    response = requests.post("https://chatbotlogisticsone-fb340de3b466.herokuapp.com/api/orders/create-order", json=payload).json()
    return json.dumps(response)

def define_agent():
    model = Groq(id="llama-3.3-70b-versatile")
    model_to_use = os.getenv('PACO_AI_MODEL')
    if model_to_use == 'GPT':
        model = OpenAIChat(id="gpt-4o-mini")
    return model


def get_paco(client_id, propmt, options):
    model = define_agent()

    return Agent(
        # Basic config
        model=model,
        show_tool_calls=True,
        debug_mode=True,
        # Training config
        tools=[get_catalog, create_purchase],
        description="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
        instructions= [
            "You should always respond in spanish",
            "Your name is Paco", 
            'When you greet the users always specify that they can end the conversation by typing "terminar"'  
            "You are an assitant in an optic center", 
            "You are able to answer questions about the available products on the optic center"
            "If you get questions about the product catalog you can use the get_catalog tool to obtain the list of available products in the optic center",
            "If the users asks you to make a puchase you can use the tool create_purchase to make the purchase on behalf of the user"
            "If the client wishes to end the conversation or return to the previous menu, you should reply END_CONVERSATION without anything else"
            "If the client wishes to talk to a human agent, you should reply HUMAN_AGENT_REQUESTED without anything else"
            "The user_id of the client is "+client_id
        ],
        # Memory config
        storage= SqlAgentStorage(table_name="agent_sessions", db_file="tmp/storage/paco/agent_storage.db"),
        memory=AgentMemory(
            db=SqliteMemoryDb(table_name="agent_memory", db_file="tmp/storage/paco/agent_storage.db"), create_user_memories=True, create_session_summary=True
        ),
        session_id=client_id,
        add_history_to_messages=True,
        num_history_responses=3
    )