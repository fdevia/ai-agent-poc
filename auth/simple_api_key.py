import os

class AuthenticationException(Exception):
    pass

def validate_simple_api_key(request):
    received_api_key = request.META.get('HTTP_AUTHORIZATION')
    api_key = os.getenv('API_KEY')
    if api_key != received_api_key:
        raise AuthenticationException("Invalid API key")
    return