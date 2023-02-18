from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .twilio_con import t
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



@csrf_exempt
def searchUsers(request):
    res = arango_con.getUsersBySubstring(
        json.loads(request.body)['substr']
    ).batch()
    return JsonResponse({ 'users': list(res) })



@csrf_exempt
def getFriends(request):
    res = arango_con.getFriendsList(
        json.loads(request.body)['id']
    ).batch()
    return JsonResponse({ 'friends': list(res) })

@csrf_exempt
def getPendingFriends(request):
    res = arango_con.getPendingFriendsList(
        json.loads(request.body)['id']
    ).batch()
    return JsonResponse({ 'pending': list(res) })

@csrf_exempt
def acceptFriend(request):
    res = arango_con.acceptFriendRequest(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({})

@csrf_exempt
def rejectFriend(request):
    res = arango_con.rejectFriendRequest(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({})

# @csrf_exempt
# def requestFriend(request):
#     res = arango_con.sendFriendRequest(
#         json.loads(request.body)['id']
#         ## TODO: Get the user ID who is requesting the friend and put it here!!
#     )

#     return JsonResponse({
#         'status': 'failed!'
#     })