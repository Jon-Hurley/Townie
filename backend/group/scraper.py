from django.http import JsonResponse
import googlemaps
import json
import os
from django.views.decorators.csrf import csrf_exempt
from . import queries

@csrf_exempt
def map(request):
    #Allows inputs for the settings:
    # input['gameKey']
    # input['settings']['theme']
    # input['settings']['radius']
    # input['settings']['lat']
    # input['settings']['lng']
    # input['settings']['length']
    # !!! ONLY ONE OF THESE WILL BE TRUE !!!
    # input['settings']['walkingAllowed']
    # input['settings']['drivingAllowed']
    # input['settings']['bicyclingAllowed']
    # input['settings']['transitAllowed']

    #try:
        list = []
        gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
        input = json.loads(request.body)
        mode = ""
        if input['settings']['drivingAllowed']:
            mode = "driving"
        elif input['settings']['walkingAllowed']:
            mode = "walking"
        elif input['settings']['bicyclingAllowed']:
            mode = "bicycling"
        elif input['settings']['transitAllowed']:
            mode = "transit"
        place_info = json.dumps(gmaps.places(input['settings']['theme'], (input['settings']['lat'], input['settings']['lng']), input['settings']['radius']))
        place3 = json.loads(place_info)
        for i in range(len(place3['results'])): #used to be len(place3['results'])
            name_dest = place3['results'][i]['name']
            latitude = place3['results'][i]['geometry']['location']['lat']
            longitude = place3['results'][i]['geometry']['location']['lng']
            queries.createDestination(latitude, longitude, name_dest, input['settings']['theme'])
            destination = dict(name=name_dest, location=[latitude, longitude]) #used to have an address as well
            list.append(destination)
        radius = float(input['settings']['radius'])
        list2 = queries.getNearbyDestinations(input['settings']['lat'], input['settings']['lng'], radius)
        dblist = [doc for doc in list2]
        for i in range(len(dblist)): #used to be len(dblist)
            thing = dblist[i]
            name = thing['name']
            lat = float(thing['latitude'])
            lng = float(thing['longitude'])
            new_loc = dict(name=name, location=[lat, lng])
            if new_loc not in list:
                list.append(new_loc)
        locationList = []
        for i in range(len(list)):
            locationList.append(list[i]['location'])
        max_time = input['settings']['length']
        time_spent = 0
        origin = dict(lat=input['settings']['lat'], lng=input['settings']['lng'])
        orderedList = []
        lengthToUse = len(list)
        if lengthToUse > 25:
            lengthToUse = 25
        min_times = []
        for i in range(lengthToUse):
            min_time = 100000000
            listDurations = []
            index = 0
            distances = gmaps.distance_matrix(origin, locationList, mode, None, None, "imperial", None, None, None, None, None)
            for j in range(len(distances['rows'][0]['elements'])):
                listDuration = int(distances['rows'][0]['elements'][j]['duration']['text'][0])
                listDurations.append(listDuration)
            for j in range(len(listDurations)):
                if listDurations[j] < min_time:
                    min_time = listDurations[j]
                    index = j
            min_times.append(min_time)
            orderedList.append(list[index])
            list.pop(index)
            origin = dict(lat=locationList[index][0], lng=locationList[index][1])
            locationList.pop(index)
            time_spent += min_time
        while time_spent > max_time:
            min_in_max = 0
            index = 0
            for i in range(len(min_times)):
                if min_in_max < min_times[i]:
                    min_in_max = min_times[i]
                    index = i
            orderedList.pop(index)
            min_times.pop(index)
            time_spent -= min_in_max
        listDict = dict(Destinations=orderedList, trueCompletionTime=time_spent)
        queries.insertIntoItinerary(listDict, input['gameKey'])
        return JsonResponse({"success": True, "timeToCompletion": time_spent})
    #except:
        #return JsonResponse({"success": False})