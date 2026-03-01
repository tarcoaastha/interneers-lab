from django.http import JsonResponse
from .service import generate_greetings 
def greeting_view(request):
    """
    A simple view that returns a greeting message as JSON.
    """
    name = request.GET.get("name", "")
    message = generate_greetings(name)
    return JsonResponse({"Message": message})