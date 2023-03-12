import { get, writable } from 'svelte/store';
import { PUBLIC_BACKEND_WS } from '$env/static/public';

export const userStore = writable();

export const mapStore = writable();

export const gamePage = writable('/game/join');

export class Game {
    static store = writable();
    /** @type {WebSocket} */
    static ws = undefined;
    static interval = undefined;

    static send(method, data) {
        const objStr = JSON.stringify({ method, ...data });
        this.ws.send(objStr);
    }

    static setDefaultEvents() {
        this.ws.onmessage = (m) => {
            const res = JSON.parse(m.data);
            console.log("WS MESSAGE:", res);
            switch (res.method) {
                case 'get-game':
                case 'update-game': {
                    this.store.set(res.data);
                    return;
                }
                default: {
                    console.log("No response behavior")
                }
            }            
        };
        this.ws.onerror = (e) => {
            console.log("WS ERROR:", e);
        }
        this.ws.onclose = () => {
            this.ws = undefined;
            this.store.set(null);
        }
    }
    
    static resumePolling() {
        this.setDefaultEvents();
        this.stopPolling();
        this.interval = setInterval(() => {
            this.send('get-game', {
                gameKey: get(this.store).game._key
            });
        }, 10000);
    }
    
    static stopPolling() {
        clearInterval(this.interval);
        this.interval = undefined;
    }

    static async join(gameKey) {
        try {
            const userKey = get(userStore).key;
            this.ws = new WebSocket(`${PUBLIC_BACKEND_WS}?gameKey=${gameKey}&userKey=${userKey}`);
            await new Promise((res, rej) => { 
                this.ws.onerror = () => rej();
                this.ws.onopen = () => res();
            });
    
            this.send('get-game', { gameKey });
            const res = await new Promise((res, rej) => { 
                this.ws.onerror = () => rej();
                this.ws.onmessage = (m) => {
                    console.log(m)
                    const { method, data } = JSON.parse(m.data);
                    if (method !== 'get-game') return;
                    if (!data?.game?._key) rej();
                    res(data);
                };
            });
            this.store.set(res);

            this.setDefaultEvents();
            return null;
        } catch (err) {
            console.log(err);
            this.ws?.close();
            this.ws = undefined;
            return "Unable to connect to lobby. Please try again.";
        }
    };

    static leave() {
        try {
            this.stopPolling();
            this.store.set(null);
            this.ws?.close();
            return true;
        } catch (err) {
            console.log(err);
            return false;
        }
    };
    
    static start() {
        try {
            const gameKey = get(this.store).game._key;
            const settings = get(this.store).game.settings;
            this.send('start-game', { gameKey, settings });
            resumePolling();
        } catch (err) {
            console.log(err);
        }
    };
    
    static awardPoints(destinationIndex) {
        try {
            const gameKey = get(this.store).game._key;
            this.send('award-points', { gameKey, destinationIndex });
        } catch (err) {
            console.log(err);
        }
    };
    
    static updateLocation(lon, lat) {
        try {
            this.send('update-location', { lon, lat });
        } catch (err) {
            console.log(err);
        }
    };
    
    static updateSettings(form) {
        try {
            const gameKey = get(this.store).game._key;
            this.send('update-settings', { gameKey, settings: form });
        } catch (err) {
            console.log(err);
        }
    };

    static getPage() {
        return get(this.store)?.game?.page || 'join'
    }
};

export class Location {
	static store = writable();
    static interval = undefined;

	static subscribe(mapState) {
		const onLocationUpdate = (loc) => {
			const { latitude: lat, longitude: lng } = loc.coords;
			const oldLoc = get(this.store);

			if (!mapState.snapLocation) {
				if (lat === oldLoc?.lat && lng === oldLoc?.lng) {
					return;
				}
			}

			console.log('setting location store...');
			this.store.set({ lat, lng });
		};

		this.interval = setInterval(() => {
			navigator.geolocation.getCurrentPosition(onLocationUpdate);
		}, 1000);

		const setMapCenter = ({ location }) => {
			if (!(location?.lat && location?.lng)) return;
			const center = new google.maps.LatLng(location.lat, location.lng);
			mapState.map.panTo(center);
		};

		return this.store.subscribe(setMapCenter);
	}

	static unsubscribe() {
		clearInterval(this.interval);
	}
};