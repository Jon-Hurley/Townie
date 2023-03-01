from django.http import JsonResponse
import googlemaps
import json
import os

@csrf_exempt
def map(request):
    list = []
    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
    #places = json.dumps(gmaps.find_place(str("Purdue University"),str("textquery")))
    #places2 = json.loads(places)
    stuff = json.loads(request.body)
    #print(places2)
    #result = json.dumps(gmaps.geocode(str('900 John R Wooden Dr, West Lafayette, IN 47907')))
    #print(result)
    #result2 = json.loads(result)

    #addressComponents = result2[0]['formatted_address']
    #print(addressComponents)
    #latitude = result2[0]['geometry']['location']['lat']
    #longitude = result2[0]['geometry']['location']['lng']
    place_info = json.dumps(gmaps.places(stuff['theme'], (stuff['lat'], stuff['lng']), stuff['radius']))
    place3 = json.loads(place_info)
    #print(place3)
    #print(place3['results'][0])
    #place4 = json.dumps(gmaps.place(place3['results'][0]['place_id']))
    #place5 = json.loads(place4)
    #print(len(place_info))
    #print(place3)
    for i in range(len(place3['results'])):
        name_dest = place3['results'][i]['name']
        #print(name_dest)
        #address = place3['results'][i]['formatted_address']
        latitude = place3['results'][i]['geometry']['location']['lat']
        longitude = place3['results'][i]['geometry']['location']['lng']
        points = 1000
        arango_con.createDestination(latitude, longitude, name_dest, points, stuff['theme'])
        destination = dict(name=name_dest, location=[latitude, longitude], pts=points) #used to have an address as well
        list.append(destination)
    radius = float(stuff['radius'])
    list2 = arango_con.getNearbyDestinations(latitude, longitude, radius)
    dblist = [doc for doc in list2]
    for i in range(len(dblist)):
        thing = dblist[i]
        name = thing['name']
        points = 1000
        lat = float(thing['latitude'])
        lng = float(thing['longitude'])
        new_loc = dict(name=name, location=[lat, lng], pts=points)
        if new_loc not in list:
            list.append(new_loc)




    return JsonResponse(list,safe=False)