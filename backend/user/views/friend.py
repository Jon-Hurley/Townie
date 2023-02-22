from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.queries import *
import json

@csrf_exempt
def getFriends(request):
    res = getFriendsList(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({ 'friends': list(res) })

@csrf_exempt
def getPendingFriends(request):
    res = getPendingFriendsList(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({ 'pending': list(res) })


@csrf_exempt
def acceptFriend(request):
    res = acceptFriendRequest(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({})

@csrf_exempt
def rejectFriend(request):
    res = rejectFriendRequest(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({})


@csrf_exempt
def requestFriend(request):
    res = sendFriendRequest(
        json.loads(request.body)['toKey'],
        json.loads(request.body)['fromKey']
    )
    return JsonResponse({'key': res['_key']})