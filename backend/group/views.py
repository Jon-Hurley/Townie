from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import redis_con

# CONNECT:
def connect(request):
    print(request)
    return JsonResponse({})

def createGroup():
    return JsonResponse({})

def joinGroup():
    return JsonResponse({})

# DISCONNECT:

def disconnect(request):
    print(request)
    return leaveGroup(request)

def leaveGroup(request):
    return JsonResponse({})

# DEFAULT

def default(request):
    return JsonResponse({})