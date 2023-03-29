import { writable, get } from 'svelte/store';
import { userStore } from './stores.js';
import { PUBLIC_BACKEND_WS } from '$env/static/public';
import { Map } from './Map.js';
import { Location } from './Location.js';

export class Game {
    static store = writable();
    /** @type {WebSocket} */
    static ws = undefined;
    static interval = undefined;

    static send(method, data) {
        const objStr = JSON.stringify({ method, ...data });
        Game.ws.send(objStr);
    }

    static setDefaultEvents() {
        Game.ws.onmessage = (m) => {
            const res = JSON.parse(m.data);
            console.log("WS MESSAGE:", res);
            switch (res.method) {
                case 'get-game':
                case 'update-game': {
                    console.log("In game.js update game")
                    console.log(res.data.players[0].destinationIndex)
                    Game.store.set(res.data);

                    console.log(Map.map)

                    if (Map.map) {

                        console.log("We zoomin")

                        Map.generateUserMarker();
    	                Map.generateDestinationCircle();
                        Map.generatePlayerMarkers();

                        Map.setZoomAndCenter();
                    }

                    console.log(get(Game.store));
                    return;
                }
                default: {
                    console.log("No response behavior")
                }
            }            
        };
        Game.ws.onerror = (e) => {
            console.log("WS ERROR:", e);
        }
        Game.ws.onclose = () => {
            Game.ws = undefined;
            Game.store.set(null);
        }
    }
    
    static resumePolling() {
        Game.setDefaultEvents();
        Game.stopPolling();
        
        Game.interval = setInterval(() => {
            console.log(get(Game.store))
            Game.send('get-game', {
                gameKey: get(Game.store).game._key
            });
        }, 10000);
    }
    
    static stopPolling() {
        clearInterval(Game.interval);
        Game.interval = undefined;
    }

    static async join(gameKey) {
        try {
            const userLocation = await Location.getCurrentLocation();
            const user = get(userStore);
            const userKey = user.key;
            user.token = "123";
            Game.ws = new WebSocket(`${PUBLIC_BACKEND_WS}?gameKey=${gameKey}&token=${user.token}
                                    &lat=${userLocation.coords.latitude}&lon=${userLocation.coords.longitude}`);
            await new Promise((res, rej) => { 
                Game.ws.onerror = () => rej();
                Game.ws.onopen = () => res();
            });

    
            Game.send('get-game', { gameKey });
            const res = await new Promise((res, rej) => { 
                Game.ws.onerror = () => rej();
                Game.ws.onmessage = (m) => {
                    console.log(m)
                    const { method, data } = JSON.parse(m.data);
                    if (method !== 'get-game') return;
                    if (!data?.game?._key) rej();
                    res(data);
                };
            });
            Game.store.set(res);

            Game.setDefaultEvents();
            return null;
        } catch (err) {
            console.log(err);
            Game.ws?.close();
            Game.ws = undefined;
            return "Unable to connect to lobby. Please try again.";
        }
    }

    static leave() {
        try {
            Game.stopPolling();
            Game.store.set(null);
            Game.ws?.close();
            return true;
        } catch (err) {
            console.log(err);
            return false;
        }
    }
    
    static start() {
        try {
            const gameKey = get(Game.store).game._key;
            const settings = get(Game.store).game.settings;
            Game.send('start-game', { gameKey, settings });
            Game.resumePolling();
        } catch (err) {
            console.log(err);
        }
    }
    
    static awardPoints(destinationIndex) {
        try {
            const gameKey = get(Game.store).game._key;
            Game.send('award-points', { gameKey, destinationIndex });
        } catch (err) {
            console.log(err);
        }
    }
    
    static updateLocation(lon, lat) {
        try {
            Game.send('update-location', {
                lon, lat,
                gameKey: get(Game.store).game._key,
                userKey: get(userStore).key
            });
        } catch (err) {
            console.log(err);
        }
    }
    
    static updateSettings(form) {
        try {
            const gameKey = get(Game.store).game._key;
            Game.send('update-settings', { gameKey, settings: form });
        } catch (err) {
            console.log(err);
        }
    }

    static getPage() {
        return get(Game.store)?.game?.page || 'join'
    }

    static getPlayer(username) {
        console.log("This is the game store")
        console.log(get(Game.store))
        /** @type {Array} */
        let pps = get(Game.store)?.players;

        return pps.find(pp => pp.username === username);
    }

    static getPlayers() {
        return get(Game.store)?.players;
    }
};