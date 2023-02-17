import { get, writable } from 'svelte/store';
import { PUBLIC_BACKEND_WS } from '$env/static/public';

export const groupStore = writable();
export const userStore = writable();

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

export const subscribeToLocation = (callback) => {
    let interval;
    
    const onLocationUpdate = (loc) => {
        const {
            latitude: lat,
            longitude: lng
        } = loc.coords;
        const oldLoc = get(locationStore).location;

        // REMOVE THIS BLOCK IF YOU WANT AUTO-RECENTER
        if (lat === oldLoc?.lat && lng === oldLoc?.lng) {
            return;
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

    locationStore.subscribe(callback);
}

export const unsubscribeToLocation = () => {
    const locObj = get(locationStore);
    clearInterval(locObj?.interval);
}