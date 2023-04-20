from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import json
import twilio_con
import util

@csrf_exempt
def getFriends(request):
    body = json.loads(request.body)

    user, newToken = util.decodeUserJWT(body['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)
    
    res = queries.getFriendsList(
        body['key']
    ).batch()

    return JsonResponse({
        'friends': list(res),
        'token': newToken
    })

@csrf_exempt
def getUsersInGames(request):
    print("HELLO WORLD")
    body = json.loads(request.body)

    user, newToken = util.decodeUserJWT(body['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)
    
    res = queries.getUsersInGame(
        body['key']
    ).batch()[0]


    return JsonResponse({
        'onlinePlayers': res,
        'token': newToken
    })

@csrf_exempt
def getPendingFriends(request):
    body = json.loads(request.body)

    user, newToken = util.decodeUserJWT(body['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)

    res = queries.getPendingFriendsList(
        user['key']
    ).batch()

    return JsonResponse({ 
        'pending': list(res),
        'token': newToken                
    })


@csrf_exempt
def acceptFriend(request):
    body = json.loads(request.body)

    user, newToken = util.decodeUserJWT(body['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)
    
    res = queries.acceptFriendRequest(
        json.loads(request.body)['key']
    ).batch()[0]
    
    message = res['originUsername'] + ' accepted your friend request!'
    twilio_con.sendNotification(
        phone=res['targetPhone'],
        message=message
    )

    return JsonResponse({
        'token': newToken
    })

@csrf_exempt
def rejectFriend(request):
    body = json.loads(request.body)

    user, newToken = util.decodeUserJWT(body['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)
    
    print(body)
    res = queries.rejectFriendRequest(
        body['key']
    ).batch()[0]
    
    message = res['originUsername'] + ' has rejected your friendship! No one likes you :(.'
    twilio_con.sendNotification(
        phone=res['targetPhone'],
        message=message
    )
    return JsonResponse({
        'token': newToken
    })

@csrf_exempt
def requestFriend(request):
    body = json.loads(request.body)
    toKey = body['toKey']

    user, newToken = util.decodeUserJWT(body['token'])
    if user is None:
        return util.returnError('Invalid token.', 401)

    docs = queries.sendFriendRequest(
        toKey,
        user['key']
    ).batch()

    if len(docs) != 1:
        return util.returnError("Invalid friend key.", 404)
    
    res = docs[0]
    message = res['originUsername'] + ' has requested to be your friend!'
    twilio_con.sendNotification(
        phone=res['targetPhone'],
        message=message
    )

    return JsonResponse({
        'token': newToken
    })