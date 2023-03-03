import { get, writable } from 'svelte/store';

export const userStore = writable();

export const gameStore = writable(
//    game: {
//    "maxTime": 0,
//    "numFinished": 0,
//    "page": "lobby",
//    "settings": {
//      "radius": 5,
//      "walkingAllowed": true,
//      "drivingAllowed": false,
//      "bicyclingAllowed": false,
//      "transitAllowed": false,
//      "theme": "None",
//      "desiredCompletionTime": 180,
//      "lon": 0,
//      "lat": 0
//    },
//    "startTime": 0,
//    "trueCompletionTime": 0
//  },
//destinations: [{
//    "latitude": 38.2555867,
//    "longitude": -85.7585581,
//    "name": "Vincenzo's",
//    "theme": "restaurant"
//  }, {
//    "latitude": 38.2581251,
//    "longitude": -85.7571317,
//    "name": "Swizzle Dinner & Drinks",
//    "theme": "restaurant"
//  }, {
//    "latitude": 38.2560922,
//    "longitude": -85.75278279999999,
//    "name": "Merle's Whiskey Kitchen",
//    "theme": "restaurant"
//  }],
//players: [{
//    "connectionId": "BKlHAczWIAMCKiQ=",
//    "destinationIndex": 0,
//    "points": 0,
//    "lon": 0,
//    "lat": 0
//  }]
//}
);

export const locationStore = writable();

export const subscribeToLocation = (mapState) => {
    let interval;
    
    const onLocationUpdate = (loc) => {
        const {
            latitude: lat,
            longitude: lng
        } = loc.coords;
        const oldLoc = get(locationStore).location;

        if (!mapState.snapLocation) {
            if (lat === oldLoc?.lat && lng === oldLoc?.lng) {
                return;
            }
        }

        console.log("setting location store...")
        locationStore.set({
            interval,
            location: { lat, lng }
        });
    }

    interval = setInterval(() => {
        navigator.geolocation.getCurrentPosition(
            onLocationUpdate
        );
    }, 1000);

    locationStore.set({ interval });

    const setMapCenter = ({ location }) => {
        if (!(location?.lat && location?.lng)) return;
        const center = new google.maps.LatLng(
            location.lat, location.lng
        );
        mapState.map.panTo(center);
    }

    locationStore.subscribe(setMapCenter);
}

export const unsubscribeToLocation = () => {
    const locObj = get(locationStore);
    clearInterval(locObj?.interval);
}

export const mapStore = writable();

export const gamePage = writable('/game/join');