import { get, writable } from 'svelte/store';
import { PUBLIC_BACKEND_WS } from '$env/static/public';

export const groupStore = writable();
export const userStore = writable({
    id: 'User/10942',
    key: '10942',
    passwordHash: 'password',
    phone: '+13176909263',
    points:	50,
    purchases: [],
    rank: 'explorer',   
    username: 'ArnavSuccs'
});

export const logout = () => {

}

export const login = () => {

}

export const autoLogin = () => {

}

export const signin = () => {

}

let ws;

export const joinLobby = () => {
    ws = new WebSocket(PUBLIC_BACKEND_WS)
    console.log(ws)
}



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
        // locationStore.set({
        //     interval,
        //     location: { lat, lng }
        // });
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