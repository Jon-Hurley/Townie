import googlemaps
import json
import os
from . import queries
import dotenv

dotenv.load_dotenv()

def map(settings, gameKey):
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
    budget = settings['budget'] if 'budget' in settings else 1

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
    
    place_info = json.dumps(gmaps.places(settings['theme'], (settings['lat'], settings['lon']), settings['radius'], None, None, budget))
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
    origin = dict(lat=settings['lat'], lng=settings['lon'])
    locationList.append(origin)
    for i in range(len(list)):
        locationList.append(list[i]['location'])
    
    orderedList = []
    lengthToUse = len(list)
    if lengthToUse > 10:
        lengthToUse = 10
    while len(locationList) > lengthToUse:
        locationList.pop()
    
    min_times = []
    print(locationList, locationList, mode)
    distances = gmaps.distance_matrix(locationList, locationList, mode, None, None, "imperial")
    print(distances)
    marked_indices = []
    for i in range(len(distances['rows'])):
        min_time = 10000000000000000000000
        index = 0
        for j in range(len(distances['rows'][i]['elements'])):
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