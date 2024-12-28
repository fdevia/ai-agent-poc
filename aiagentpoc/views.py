from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from aiagentpoc.agents.agents import available_agents
import json


@csrf_exempt
def example_endpoint(request):
    body = json.loads(request.body.decode('utf-8'))
    load_dotenv()
    try:
        agent_name = body["agent"]
        client_prompt = body["prompt"]

        agent = available_agents.get(agent_name)
        if agent == None:
            return JsonResponse({
            "error": "Agent not found",
        })
        
        agent_response = agent.run(client_prompt)
        suggested_response = agent_response.messages[-1].content

        return JsonResponse({
            "agentResponse": suggested_response,
        })
    except Exception as e:
        print("Error in handler", e)
        data = {
            "agentResponse": "Lo siento, en este momento no me encuentro disponible. Intentalo de nuevo más tarde",
        }
        return JsonResponse(data)