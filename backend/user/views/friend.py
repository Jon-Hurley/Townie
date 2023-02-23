from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import json

@csrf_exempt
def getFriends(request):
    res = queries.getFriendsList(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({ 'friends': list(res) })

@csrf_exempt
def getPendingFriends(request):
    res = queries.getPendingFriendsList(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({ 'pending': list(res) })


@csrf_exempt
def acceptFriend(request):
    res = queries.acceptFriendRequest(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({})

@csrf_exempt
def rejectFriend(request):
    res = queries.rejectFriendRequest(
        json.loads(request.body)['key']
    ).batch()
    return JsonResponse({})


@csrf_exempt
def requestFriend(request):
    res = queries.sendFriendRequest(
        json.loads(request.body)['toKey'],
        json.loads(request.body)['fromKey']
    )
    return JsonResponse({'key': res['_key']})