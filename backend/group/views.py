from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import redis_con
import googlemaps
import json
import os
import arango_con

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

# CREATE A LOBBY/GAME

def createLobby(request):
    startTime = json.loads(request.body)['startTime']
    maxTime = json.loads(request.body)['maxTime']
    intendedCompletionTime = json.loads(request.body)['intendedCompletionTime']

    group = json.loads(request.body)['group']

    destinations = json.loads(request.body)['destinations']

    transportation = []
    transportation.append(json.loads(request.body)['busAllowed'])
    transportation.append(json.loads(request.body)['carAllowed'])
    transportation.append(json.loads(request.body)['subwayAllowed'])
    transportation.append(json.loads(request.body)['boatAllowed'])

    radius = json.loads(request.body)['radius']

    theme = json.loads(request.body)['theme']

    res = arango_con.createLobby(startTime, maxTime, group, destinations, transportation, radius, intendedCompletionTime, theme)

    return JsonResponse({
        'key': res['_key']
    })

@csrf_exempt
def map(request):
    list = []
    #print(request)
    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
    places = json.dumps(gmaps.find_place(str("Purdue University"),str("textquery")))
    places2 = json.loads(places)

    #print(places2)
    result = json.dumps(gmaps.geocode(str('900 John R Wooden Dr, West Lafayette, IN 47907')))
    #print(result)
    result2 = json.loads(result)

    addressComponents = result2[0]['formatted_address']
    #print(addressComponents)
    latitude = result2[0]['geometry']['location']['lat']
    longitude = result2[0]['geometry']['location']['lng']
    place_info = json.dumps(gmaps.places("art museum", (latitude,longitude)))
    place3 = json.loads(place_info)
    #print(place3)
    #print(place3['results'][0])
    place4 = json.dumps(gmaps.place(place3['results'][0]['place_id']))
    place5 = json.loads(place4)
    #print(len(place_info))
    print(place3)
    for i in range(len(place3['results'])):
        name_dest = place3['results'][i]['name']
        print(name_dest)
        address = place3['results'][i]['formatted_address']
        latitude = place3['results'][i]['geometry']['location']['lat']
        longitude = place3['results'][i]['geometry']['location']['lng']

        points = 1000
        destination = dict(name=name_dest, addr=address, location=[latitude, longitude], pts=points)
        list.append(destination)
        #print(destination)
    #location = Location
    #location.latitude = latitude
    #location.longitude = longitude
    #print(latitude)



    return JsonResponse(list,safe=False)