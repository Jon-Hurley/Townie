from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .twilio_con import t
import arango_con

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

@csrf_exempt
def searchUsers(request):
    res = arango_con.getUsersBySubstring(
        request.body.substr
    )
    # print()
    return JsonResponse({
        'res': 'hi'
    })

def requestFriend(request):
    return JsonResponse({
        'status': 'failed!'
    })

def acceptFriend(request):
    return JsonResponse({
        'newFriendsList': []
    })

def removeFriend(request):
    return JsonResponse({
        'newFriendsList': []
    })