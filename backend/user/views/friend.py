from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import user.queries as queries
import os
import json
from twilio.rest import Client

def sendRequestNotif(username, otherPhone):
    client = Client(os.environ.get('TWILIO_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    notification = client.notify.services('ISbae49bcc3d2a7d2651bb66a1adc054ec').notifications.create(
        to_binding='{"binding_type":"sms", "address":'+otherPhone+'}',
        body='Townie: '+username+' has sent you a friend request!')
    print(notification.sid)

def acceptRequestNotif(username, otherPhone):
    client = Client(os.environ.get('TWILIO_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    notification = client.notify.services('ISbae49bcc3d2a7d2651bb66a1adc054ec').notifications.create(
        to_binding='{"binding_type":"sms", "address":'+otherPhone+'}',
        body='Townie: '+username+' has accepted your friend request!')
    print(notification.sid)

def denyRequestNotif(username, otherPhone):
    client = Client(os.environ.get('TWILIO_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    notification = client.notify.services('ISbae49bcc3d2a7d2651bb66a1adc054ec').notifications.create(
        to_binding='{"binding_type":"sms", "address":'+otherPhone+'}',
        body='Townie: '+username+' has denied your friend request!')
    print(notification.sid)

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
    data = json.loads(request.body)
    res = queries.acceptFriendRequest(
        data['key']
    ).batch()[0]

    acceptRequestNotif(data['username'], res['phone'])

    return JsonResponse({})

@csrf_exempt
def rejectFriend(request):
    data = json.loads(request.body)
    res = queries.rejectFriendRequest(
        data['key']
    ).batch()[0]

    denyRequestNotif(data['username'], res['phone'])

    return JsonResponse({})


@csrf_exempt
def requestFriend(request):
    data = json.loads(request.body)
    res = queries.sendFriendRequest(
        data['toKey'],
        data['fromKey']
    )

    sendRequestNotif(data['username'], data['toPhone'])

    return JsonResponse({'key': res['_key']})