
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

    Each dictionary contains details about a specific product, including its SKU, brand, material, design, size, 
    description, color, and price. This function simulates a database or API call to retrieve product data.

    Returns:
        list: A list of dictionaries, each representing a product. Each dictionary contains the following keys:
            - "sku" (str): The unique stock keeping unit identifier of the product.
            - "padre" (str): The identifier of the parent product or category.
            - "marca" (str): The brand of the product.
            - "material" (str): The material used for the product.
            - "diseno" (str): The design type of the product.
            - "detallecolor" (str): The specific color detail of the product.
            - "aro" (str): The size of the frame or item (for eyewear, for example).
            - "puente" (str): The bridge size (for eyewear).
            - "vertical" (str): The vertical size of the product.
            - "genero" (str): The gender category for the product (e.g., "MUJER" for women).
            - "qty" (str): The quantity available for the product.
            - "descripcion" (str): A brief description of the product.
            - "color" (str): The color of the product.
            - "precioventa" (str): The retail price of the product.
"""
def get_catalog():
    response = requests.get("https://gist.githubusercontent.com/fdevia/006cd15217844493eba46be7095a7891/raw/4203f3e684b9463ab05ce13df6ac53f6dbfc29e9/productosopticas.json").json()
    return json.dumps(response)

def define_agent():
    model = Groq(id="llama-3.3-70b-versatile")
    model_to_use = os.getenv('PACO_AI_MODEL')
    if model_to_use == 'GPT':
        model = OpenAIChat(id="gpt-4o-mini")
    return model


def get_paco(client_id):
    model = define_agent()

    return Agent(
        # Basic config
        model=model,
        show_tool_calls=True,
        debug_mode=True,
        # Training config
        tools=[get_catalog],
        description="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
        instructions= [
            "You should always respond in spanish",
            "Your name is Paco", 
            "You are an assitant in a optic center", 
            "You are able to answer questions about the available products on the optic center"
            "If you get questions about the product catalog you can use the get_catalog tool to obtain the list of available products in the optic center",
            "If the client wishes to end the conversation or return to the previous menu, you should reply END_CONVERSATION without anything else"
            "If the client wishes to talk to a human agent, you should reply HUMAN_AGENT_REQUESTED without anything else"
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