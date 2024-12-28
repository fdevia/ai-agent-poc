from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from aiagentpoc.agents.agents import available_agents
from auth.simple_api_key import validate_simple_api_key, AuthenticationException
import json


@csrf_exempt
def post_prompt(request):
    load_dotenv()

    try:
        validate_simple_api_key(request)
        
        body = json.loads(request.body.decode('utf-8'))
        agent_name = body["agent"]
        client_prompt = body["prompt"]

        agent = available_agents.get(agent_name)
        if agent == None:
            return HttpResponseNotFound("Agent not found")
        
        agent_response = agent.run(client_prompt)
        suggested_response = agent_response.messages[-1].content

        return JsonResponse({
            "agentResponse": suggested_response,
        })
    except AuthenticationException as e:
        print("Auth error:", e)
        return HttpResponseForbidden("Forbidden")
    except Exception as e:
        print("Error in handler:", e)
        return JsonResponse({
            "agentResponse": "Lo siento, en este momento no me encuentro disponible. Intentalo de nuevo más tarde",
        })