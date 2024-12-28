import os
from dotenv import load_dotenv

class AuthenticationException(Exception):
    pass

def validate_simple_api_key(request):
    load_dotenv()
    api_key = os.getenv('API_KEY')

    received_api_key = request.META.get('HTTP_AUTHORIZATION')
    
    if api_key != received_api_key:
        raise AuthenticationException("Invalid API key")
    
    return