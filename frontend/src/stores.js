import { get, writable } from 'svelte/store';

export const userStore = writable();

export const profileStore = writable();

export const gameStore = writable();

export const locationStore = writable();

const _onLocationUpdate = (loc) => {
    const {
        latitude: lat,
        longitude: lng
    } = loc.coords;
    const oldLoc = get(locationStore).location;

    console.log("setting location store...")
    locationStore.set({
        location: { lat, lng }
    });
}

export const subscribeLocationBeforeMap = async() => {
    const res2 = await new Promise((res, rej) => { 
        navigator.geolocation.getCurrentPosition((loc) => {
            _onLocationUpdate(loc);
        });
        res(15)
    });
    
    let interval;

    interval = setInterval(() => {
        navigator.geolocation.getCurrentPosition(
            _onLocationUpdate
        );
    }, 1000);

    locationStore.set({ interval });
}

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