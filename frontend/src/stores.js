import { get, writable } from 'svelte/store';
import { PUBLIC_BACKEND_WS } from '$env/static/public';

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

export const gameStore = writable();

export const joinGame = async(gameKey) => {
    try {
        const ws = new WebSocket(`${PUBLIC_BACKEND_WS}`);
        await new Promise((res, rej) => { 
            ws.onopen = (e) => {
                gameStore.set({
                    ws,
                    gameKey
                });
                ws.onerror = (e) => {
                    console.log(e);
                    ws.close();
                }
                ws.onmessage = (m) => {
                    console.log(m)
                }
                res();
            }
            ws.onerror = (e) => {
                rej();
            }
        });
        return true;
    } catch (err) {
        console.log(err);
        return false;
    }
}

export const leaveGame = async(gameKey) => {
    try {
        /** @type {WebSocket} */
        const ws = get(gameStore).ws;
        ws.close();
        return true;
    } catch (err) {
        console.log(err);
        return false;
    }
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