import requests
import json
import os
import dotenv
# import mapbox --> Do not need for now
from . import queries
import googlemaps

dotenv.load_dotenv()

def generate(settings, gameKey):

    # Allows inputs for the settings:
    # settings['theme']
    # settings['radius']
    # settings['lat']
    # settings['lon']
    # settings['desiredCompletionTime']
    # settings['budget']
    # !!! ONLY ONE OF THESE WILL BE TRUE !!!
    # settings['walkingAllowed']
    # settings['drivingAllowed']
    # settings['bicyclingAllowed']
    # settings['transitAllowed']

    list = []
    mode = ""
    if settings['drivingAllowed']:
        mode = "driving"
    elif settings['walkingAllowed']:
        mode = "walking"
    elif settings['bicyclingAllowed']:
        mode = "bicycling"
    elif settings['transitAllowed']:
        mode = "transit"
    
    theme = 0
    if settings['theme'] == "tourist_attraction":
        theme = 10000
    elif settings['theme'] == "restaurant":
        theme = 13000
    elif settings['theme'] == "store":
        theme = 17000
    elif settings['theme'] == "museum":
        theme = 10027
    else:
        theme = 10000

    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))

    url = "https://api.foursquare.com/v3/places/search"

    lat_lng = str(settings['lat']) + "," + str(settings['lon'])
    # lat_lng_test = "40.425869,-86.908066"
    # radius_test = "100000"
    # budget_test = "4"
    # print(settings['theme'])
    params = {
        "ll": lat_lng,
        #"open_now": "true",
        "sort": "DISTANCE",
        "radius": int(settings['radius']/0.000621371),
        "max_price": settings['budget'],
        "categories": [theme],
        "limit": 50,
        "fields": "name,geocodes,categories,distance,description,website,price,menu,tips,tastes,features",
    }

    headers = {
        "Accept": "application/json",
        "Authorization": os.environ.get("TOWNIE_FSQ_KEY")
    }

    response = requests.request("GET", url, params=params, headers=headers)
    response1 = json.loads(response.text)
    # print(response1)
    # for i in range(len(response1['results'])):
    #     print(response1['results'][i]['name'])
    # print(response1) SAI: This is the response from the FSQ call. You can use this to get the data you need.

    for i in range(len(response1['results'])):
        name_dest = response1['results'][i]['name']
        latitude = response1['results'][i]['geocodes']['main']['latitude']
        longitude = response1['results'][i]['geocodes']['main']['longitude']
        tip_array = []

        for j in range(len(response1['results'][i]['tips'])):
            if (j > 2):
                break
            if (response1['results'][i]['tips'][j]['text'] != ""):
                tip_array.append(response1['results'][i]['tips'][j]['text'])
        
        queries.createDestination(latitude, longitude, name_dest, settings['theme'], tip_array)
        destination = dict(name=name_dest, location=[latitude, longitude])
        new_name = True
        for j in range(len(list)):
            if (destination['name'] == list[j]['name']):
                new_name = False
                break
        if new_name == True:
            list.append(destination)
    
    arango_list = queries.getNearbyDestinations(settings['lat'], settings['lon'], settings['radius']/0.000621371, settings['theme'])
    dblist = [doc for doc in arango_list]
    
    for i in range(len(dblist)):
        entry = dblist[i]
        name_dest = entry['name']
        lat = float(entry['latitude'])
        lng = float(entry['longitude'])
        new_loc = dict(name=name_dest, location=[lat, lng])
        new_name = True
        for j in range(len(list)):
            if new_loc['name'] == list[j]['name']:
                new_name = False
                break
        if new_name == True:
            list.append(new_loc)

    if (len(list) == 0):
        return 0
        
    # for i in range(len(list)):
    #     print(list[i]['name']) 

    locationList = []
    list_copy = []
    origin = dict(lat=settings['lat'], lng=settings['lon'])
    locationList.append(origin)
    for i in range(len(list)):
        dest = dict(lat=list[i]['location'][0], lng=list[i]['location'][1])
        locationList.append(dest)
        list_copy.append(list[i])
    orderedList = []
    lengthToUse = len(list)
    if lengthToUse > 10:
        lengthToUse = 10
    unusedList = []
    for i in range(len(locationList) - lengthToUse):
        locationList.pop()
        unusedList.append(list_copy.pop())
    
    # print("LOCATION LIST: " + str(locationList))

    # mapbox_locations = ""
    # for i in range(len(locationList)):
    #     mapbox_locations += locationList[i]['location']['']

        
    # mapbox_url = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving/-122.42,37.78;-122.45,37.91;-122.48,37.73?&sources=0&destinations=all&access_token=" + os.environ.get("PUBLIC_MAPBOX_TOKEN")
    # mapbox_headers = {
    #     "Accept": "application/json",
    # }
    # mapbox_response = requests.request("GET", mapbox_url, headers=mapbox_headers)
    # mapbox_loaded = json.loads(mapbox_response.text)
    # print("MAPBOX: " + str(mapbox_loaded))


    queries.insertIntoUnusedItinerary(unusedList, gameKey)

    min_times = []
    distances = gmaps.distance_matrix(locationList, locationList, mode, None, None, "imperial")
    marked_indices = []
    for i in range(len(distances['rows'])):
        min_time = 10000000000000000000000
        index = 0
        for j in range(len(distances['rows'][i]['elements'])):
            if distances['rows'][i]['elements'][j]['status'] == "OK": 
                if distances['rows'][i]['elements'][j]['duration']['value'] != 0 and distances['rows'][i]['elements'][j]['duration']['value'] < min_time and j not in marked_indices and j != 0:
                    min_time = distances['rows'][i]['elements'][j]['duration']['value']
                    index = j
        marked_indices.append(index)
        min_times.append(min_time)
    
    total_time = 0
    for i in range(len(marked_indices) - 1):
        new_itinerary = dict(destination=list[marked_indices[i]], time=min_times[i])
        orderedList.append(new_itinerary)
        total_time = total_time + min_times[i]
    
    while total_time > settings['desiredCompletionTime'] * 60:
        temp = orderedList.pop()
        total_time = total_time - temp['time']
    
    listDict = dict(Destinations=orderedList, trueCompletionTime=total_time)
    print("LIST DICT: " + str(listDict))
    queries.insertIntoItinerary(listDict, gameKey)
    return total_time

def extendGame(settings, gameKey):
    mode = ""
    if settings['drivingAllowed']:
        mode = "driving"
    elif settings['walkingAllowed']:
        mode = "walking"
    elif settings['bicyclingAllowed']:
        mode = "bicycling"
    elif settings['transitAllowed']:
        mode = "transit"
    
    new_time = settings['desiredCompletionTime']
    new_itineraries = queries.findUnusedItineraries(gameKey)
    new_dests = queries.findUnusedDestsFromItinerary(new_itineraries)
    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
    players = queries.findPlayers(gameKey)
    player1 = players[0]
    origin = dict(lat=player1['lat'], lng=player1['lon'])
    dests_to_compute = []
    dests_to_compute.append(origin)
    print(new_dests)
    for i in range(len(new_dests)):
        location_dict = dict(lat=new_dests[i]['latitude'], lng=new_dests[i]['longitude'])
        dests_to_compute.append(location_dict)
    length_to_use = len(dests_to_compute)

    if length_to_use > 10:
        length_to_use = 10
    
    while len(dests_to_compute) > length_to_use:
        dests_to_compute.pop()
    distances = gmaps.distance_matrix(dests_to_compute, dests_to_compute, mode, None, None, "imperial")
    ordered_dests = []
    min_times = []
    marked_indices = []
    
    for i in range(len(distances['rows'])):
        min_time = 100000000000000000
        index = 0
        added = False
        for j in range(len(distances['rows'][i]['elements'])):
            if distances['rows'][i]['elements'][j]['status'] == "OK":
                if distances['rows'][i]['elements'][j]['duration']['value'] != 0 and distances['rows'][i]['elements'][j]['duration']['value'] < min_time and j not in marked_indices and j != 0:
                    min_time = distances['rows'][i]['elements'][j]['duration']['value']
                    print(min_time)
                    index = j
                    added = True
        if added:
            marked_indices.append(index)
            min_times.append(min_time)

    game = queries.getGame(gameKey)
    game1 = [doc for doc in game]
    total_time = game1[0]['game']['trueCompletionTime']
    print(marked_indices)
    print(min_times)
    print(new_dests)
    for i in range(len(marked_indices)): # used to be len(marked_indices) - 1
        if (total_time < settings['desiredCompletionTime'] * 60):
            new_itinerary = dict(destination=new_dests[marked_indices[i]], time=min_times[i])
            ordered_dests.append(new_itinerary)
            total_time += min_times[i]
            queries.removeUnusedItinerary(new_itineraries[i], gameKey)
        else:
            break
    
    listDict = dict(Destinations=ordered_dests, trueCompletionTime=total_time)
    itinerary = queries.getItinerary(gameKey)
    itinerary1 = [doc for doc in itinerary]
    index = len(itinerary1[0]['destinations'])
    queries.insertIntoNewItinerary(listDict, gameKey, index)
    return total_time
    


def truncateGame(settings, gameKey):
    game = queries.getGame(gameKey)
    game1 = [doc for doc in game]
    total_time = game1[0]['game']['trueCompletionTime']
    itinerary = queries.getItinerary(gameKey)
    itinerary1 = [doc for doc in itinerary]
    actual_itinerary = itinerary1[0]
    unused_itinerary = []

    while settings['desiredCompletionTime'] * 60 < total_time:
        removed_dest = actual_itinerary['destinations'].pop(0)
        print("removed dest: " + str(removed_dest))
        queries.removeItinerary(removed_dest, gameKey)
        total_time -= removed_dest['timeToCompletion']
        unused_itinerary.append(removed_dest)
        
    queries.insertIntoUnusedItinerary(unused_itinerary, gameKey)
    return total_time