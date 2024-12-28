
import json
import requests
from phi.agent import Agent
from phi.model.groq import Groq

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
    return json.dumps(response[:50])

paco = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[get_catalog],
    show_tool_calls=True,
    instructions= [
        "Responder en español", 
        "Tu nombre es Paco", 
        "Eres un asistente de una optica que vende gafas", 
        "Por ahora solo puedes responder preguntas sobre el catalogo de gafas"
        "Si te hacen preguntas sobre los productos disponibles, puedes usar la herramienta get_catalog para obtener el listado de productos disponibles"
    ],
    debug_mode=True
)