from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import json
import twilio_con

def returnError(errorMessage, errCode):
    return JsonResponse(
        {
            'errorMessage': errorMessage
        },
        status=errCode
    )

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
    print(json.loads(request.body))
    res = queries.acceptFriendRequest(
        json.loads(request.body)['key']
    ).batch()[0]
    
    message = res['originUsername'] + ' accepted your friend request!'
    twilio_con.sendNotification(
        phone=res['targetPhone'],
        message=message
    )
    return JsonResponse({})

@csrf_exempt
def rejectFriend(request):
    res = queries.rejectFriendRequest(
        json.loads(request.body)['key']
    ).batch()[0]
    
    message = res['originUsername'] + ' has rescinded your friendship! No one likes you :(.'
    twilio_con.sendNotification(
        phone=res['targetPhone'],
        message=message
    )
    return JsonResponse({})

@csrf_exempt
def requestFriend(request):
    body = json.loads(request.body)
    toKey = body['toKey']
    fromKey = body['fromKey']

    docs = queries.sendFriendRequest(
        toKey,
        fromKey
    ).batch()

    if len(docs) != 1:
        return returnError("Invalid friend key.", 404)
    
    res = docs[0]
    message = res['originUsername'] + ' has requested to be your friend!'
    twilio_con.sendNotification(
        phone=res['targetPhone'],
        message=message
    )

    return JsonResponse({ 'key': res['key'] })