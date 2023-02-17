from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .redis_con import r
import googlemaps
import json
import os

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

@csrf_exempt
def map(request):
    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
    result = json.dumps(gmaps.geocode(str('900 John R Wooden Dr, West Lafayette, IN 47907')))
    result2 = json.loads(result)
    addressComponents = result2[0]['formatted_address']
    print(addressComponents)
    latitude = result2[0]['geometry']['location']['lat']
    longitude = result2[0]['geometry']['location']['lng']
    #location = Location
    #location.latitude = latitude
    #location.longitude = longitude
    print(latitude)

    return JsonResponse({"location":addressComponents,"latitude":latitude,"longitude":longitude},safe=False)
