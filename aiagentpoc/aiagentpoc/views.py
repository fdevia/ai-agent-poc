from django.http import JsonResponse

def example_endpoint(request):
    data = {
        "message": "Hello, this is your API endpoint!",
        "status": "success",
    }
    return JsonResponse(data)