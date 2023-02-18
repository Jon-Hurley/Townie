from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..twilio_con import t
import arango_con
import json

def signup(request):
    return JsonResponse({
        ":)": ":)"
    })

@csrf_exempt # note csrf is being wonky, add this to POST/PUT/DELETE reqs for now
def login(request):
    return JsonResponse({
        ":)": ":)"
    })

def loginWithToken(request):
    return JsonResponse({
        ":)": ":)"
    })


def initiatePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })

def completePasswordReset(request):
    return JsonResponse({
        ":)": ":)"
    })