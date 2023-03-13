from django.http import JsonResponse
import googlemaps
import json
import os
from django.views.decorators.csrf import csrf_exempt
from . import queries

@csrf_exempt
def map(settings, gameKey):
    # Allows inputs for the settings:
    # settings['theme']
    # settings['radius']
    # settings['lat']
    # settings['lon']
    # settings['length']
    # !!! ONLY ONE OF THESE WILL BE TRUE !!!
    # settings['walkingAllowed']
    # settings['drivingAllowed']
    # settings['bicyclingAllowed']
    # settings['transitAllowed']
        print("SETTINGS")
        print(settings)
        list = []
        gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
        mode = ""
        if settings['drivingAllowed']:
            mode = "driving"
        elif settings['walkingAllowed']:
            mode = "walking"
        elif settings['bicyclingAllowed']:
            mode = "bicycling"
        elif settings['transitAllowed']:
            mode = "transit"
        place_info = json.dumps(gmaps.places(settings['theme'], (settings['lat'], settings['lon']), settings['radius']))
        place3 = json.loads(place_info)
        for i in range(len(place3['results'])): #used to be len(place3['results'])
            name_dest = place3['results'][i]['name']
            latitude = place3['results'][i]['geometry']['location']['lat']
            longitude = place3['results'][i]['geometry']['location']['lng']
            queries.createDestination(latitude, longitude, name_dest, settings['theme'])
            destination = dict(name=name_dest, location=[latitude, longitude]) #used to have an address as well
            list.append(destination)
        radius = float(settings['radius'])
        list2 = queries.getNearbyDestinations(settings['lat'], settings['lon'], radius)
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
        max_time = settings['desiredCompletionTime']
        time_spent = 0
        origin = dict(lat=settings['lat'], lng=settings['lon'])
        orderedList = []
        lengthToUse = len(list)
        if lengthToUse > 25:
            lengthToUse = 25
        min_times = []
        distances = gmaps.distance_matrix(origin, locationList, mode, None, None, "imperial", None, None, None, None)
        print(distances)
        listDurations = [len(list)]
        print(distances['rows'])
        for i in range(len(distances['rows'][0]['elements'])):
            listDurations.append(int(distances['rows'][0]['elements'][i]['duration']['text'][0]))
        print("LIST DURATIONS")
        print(listDurations)
        min_time = 1000000000
        marked_indices = []
        index = 0
        count = 0
        while len(marked_indices) < len(listDurations):
            for i in range(len(listDurations)):
                if min_time > listDurations[i] and marked_indices.count(i) == 0:
                    min_time = listDurations[i]
                    index = i
            marked_indices.append(index)
            index = 0
            count = count + 1
        for i in range(len(marked_indices)):
            orderedList.append(list[marked_indices[i]])
        print(orderedList)

        # for i in range(lengthToUse):
        #     min_time = 100000000
        #     listDurations = []
        #     index = 0
        #     #distances = gmaps.distance_matrix(origin, locationList, mode, None, None, "imperial", None, None, None, None, None)
        #     for j in range(len(distances['rows'][0]['elements'])):
        #         listDuration = int(distances['rows'][0]['elements'][j]['duration']['text'][0])
        #         listDurations.append(listDuration)
        #     for j in range(len(listDurations)):
        #         if listDurations[j] < min_time:
        #             min_time = listDurations[j]
        #             index = j
        #     min_times.append(min_time)
        #     orderedList.append(list[index])
        #     list.pop(index)
        #     origin = dict(lat=locationList[index][0], lng=locationList[index][1])
        #     locationList.pop(index)
        #     time_spent += min_time
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
        queries.insertIntoItinerary(listDict, gameKey)
        return time_spent