import googlemaps
import json
import os
from . import queries
import dotenv
dotenv.load_dotenv()

@csrf_exempt
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
    print(int(settings['radius']/0.000621371))
    place_info = json.dumps(gmaps.places(None, (settings['lat'], settings['lon']),  int(settings['radius']/0.000621371), None, None, settings['budget'], False, settings['theme'], None, None))
    #place_info = json.dumps(gmaps.places_nearby((settings['lat'], settings['lon']),  int(settings['radius']/0.000621371), None, None, None, settings['budget'], None, False, None, settings['theme'], None))
    print(place_info)
    place3 = json.loads(place_info)
    for i in range(len(place3['results'])): #used to be len(place3['results'])
        name_dest = place3['results'][i]['name']
        latitude = place3['results'][i]['geometry']['location']['lat']
        longitude = place3['results'][i]['geometry']['location']['lng']
        queries.createDestination(latitude, longitude, name_dest, settings['theme'])
        destination = dict(name=name_dest, location=[latitude, longitude]) #used to have an address as well
        new_name = False
        for j in range(len(list)):
            if (destination['name'] == list[j]['name']):
               new_name = True 
        if not new_name:
            list.append(destination)
    
    radius = float(settings['radius'])
    list2 = queries.getNearbyDestinations(settings['lat'], settings['lon'], radius/0.000621371)
    dblist = [doc for doc in list2]
    for i in range(len(dblist)): #used to be len(dblist)
        thing = dblist[i]
        name = thing['name']
        lat = float(thing['latitude'])
        lng = float(thing['longitude'])
        new_loc = dict(name=name, location=[lat, lng])
        new_name = True
        for j in range(len(list)):
            if new_loc['name'] == list[j]['name']:
                new_name = False
        if new_name:
            list.append(new_loc)
    if len(list) == 0:
        print("No destinations were found")
        return 0
    locationList = []
    list_copy = []
    origin = dict(lat=settings['lat'], lng=settings['lon'])
    locationList.append(origin)
    for i in range(len(list)):
        locationList.append(list[i]['location'])
        list_copy.append(list[i])
    orderedList = []
    lengthToUse = len(list)
    if lengthToUse > 10:
        lengthToUse = 10
    unusedList = []
    for i in range(len(locationList) - lengthToUse):
        locationList.pop()
        unusedList.append(list_copy.pop())
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
    queries.insertIntoItinerary(listDict, gameKey)
    return total_time

@csrf_exempt
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
    for i in range(len(marked_indices) -1):
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
    
# could be errors here
@csrf_exempt
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
    
