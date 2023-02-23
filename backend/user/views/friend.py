from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import arango_con
import json


@csrf_exempt
def getFriends(request):
    res = arango_con.getFriendsList(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({ 'friends': list(res) })

@csrf_exempt
def getPendingFriends(request):
    res = arango_con.getPendingFriendsList(
        json.loads(request.body)['key']
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


@csrf_exempt
def requestFriend(request):
    res = arango_con.sendFriendRequest(
        json.loads(request.body)['toKey'],
        json.loads(request.body)['fromKey']
    )
    return JsonResponse({'key': res['_key']})