import { writable, get } from 'svelte/store';
import { pushPopup, userStore } from '../stores.js';
import { PUBLIC_BACKEND_WS } from '$env/static/public';
import { Map } from './Map.js';
import { Location } from './Location.js';
import { goto } from '$app/navigation';

export class Game {
    static store = writable();
    /** @type {WebSocket} */
    static ws = undefined;
    static interval = undefined;

    static send(method, data) {
        const objStr = JSON.stringify({ method, ...data });
        Game.ws.send(objStr);
    }

    static handleGameUpdate(data) {
        if (!data) return;
        data.destinations.sort((a, b) => a.index - b.index);
        Game.store.set(data);
        if (Map.map) {
            console.log("We zoomin");
            Map.generateUserMarker();
            Map.generateDestinationCircle();
            Map.generatePlayerMarkers();
            Map.setZoomAndCenter();
        }
    }
    static handleLocationUpdate(data) {
        console.log(data);
        const {
            destinationIndex, reached, quiet,
            time, dist, totalTime, totalDist
        } = data;

        if (!quiet && reached) {
            const achievedDest = Game.nextDestination;
            pushPopup(
                0,
                `You reached destination ${achievedDest.n}!\n
                You took ${time} minutes and traveled ${dist} miles.\n
                Total time: ${totalTime} minutes\n
                Total distance: ${totalDist} miles`
            );
            if (destinationIndex === Game.destinations.length - 1) {
                const gameKey = Game.game._key;
                Game.leave();
                pushPopup(
                    0, "You have reached the final destination. You won the game!",
                    () => goto('/summary/' + gameKey)
                );
            } else {
                Game.store.set({
                    ...get(Game.store),
                    destinationIndex: destinationIndex + 1
                });
            }
        }
    }



    static setDefaultEvents() {
        Game.ws.onmessage = (m) => {
            try {
                const { method, data } = JSON.parse(m.data);
                console.log("WS MESSAGE:", { method, data });
                switch (method) {
                    case 'get-game':
                    case 'update-game': {
                        Game.handleGameUpdate(data); return;
                    }
                    case 'update-location': {
                        Game.handleLocationUpdate(data); return;
                    }
                    default: {
                        console.log("No response behavior");
                    }
                }
            } catch (e) {
                console.log("WS ERROR:", e);
                pushPopup(0, "Connections error. Please try again later.");
            }
        };
        Game.ws.onerror = (e) => {
            console.log("WS ERROR:", e);
            pushPopup(0, "Connections error. Please try again later.");
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
            if (get(Game?.store)?.game) {
                Game.send('get-game', {
                    gameKey: get(Game.store).game._key
                });
            }
        }, 10000);
    }
    
    static stopPolling() {
        clearInterval(Game.interval);
        Game.interval = undefined;
    }

    static async join(gameKey) {
        try {
            const userLocation = await Location.getCurrentLocation();
            const params = {
                'gameKey': gameKey,
                'token': "\"" + get(userStore).token + "\"",
                'lat': userLocation.lat,
                'lon': userLocation.lng
            }
            const urlParams = new URLSearchParams(params).toString();
            Game.ws = new WebSocket(`${PUBLIC_BACKEND_WS}?${urlParams}`);
            await new Promise((res, rej) => { 
                Game.ws.onerror = () => rej();
                Game.ws.onopen = (e) => res(e);
            });
    
            Game.send('get-game', { gameKey });
            const res = await new Promise((res, rej) => { 
                Game.ws.onerror = () => rej();
                Game.ws.onmessage = (m) => {
                    try {
                        const { method, data } = JSON.parse(m.data);
                        if (method !== 'get-game') return;
                        if (!data?.game?._key) rej();
                        res(data);
                    } catch (e) {
                        rej({message: 'Invalid game key. Please try again.'});
                    }
                };
            });
            if (res.player === null) {
                throw new Error("Unable to connect to game.")
            }

            Game.store.set(res);
            Game.setDefaultEvents();
        } catch (err) {
            console.log(err);
            Game.ws?.close();
            Game.ws = undefined;
            Game.store.set(null);
            pushPopup(0, err.message || "Unable to connect to lobby. Please try again.");
        }
    }

    static leave() {
        try {
            Game.stopPolling();
            Game.ws?.close();
            Game.store.set(null);
            return true;
        } catch (err) {
            console.log(err);
            return false;
        }
    }
    
    static async start() {
        try {
            Game.stopPolling();
            Game.send('start-game', {
                gameKey: Game.game._key,
                settings: Game.game.settings
            });
            const res = await new Promise((res, rej) => {
                Game.ws.onmessage = (m) => {
                    try {
                        console.log({m})
                        const { method, data } = JSON.parse(m.data);
                        if (method === 'update-game') {
                            Game.handleGameUpdate(data);
                            if (data?.game?.page === 'map') res()
                        }
                    } catch (e) {
                        rej(e);
                    }
                }
                Game.ws.onerror = rej;
            });
            Game.resumePolling();
            return true;
        } catch (err) {
            pushPopup(0, "Unable to start game. Please try again.");
            return false;
        }
    }
    
    static updateLocation(lat, lon) {
        try {
            Game.send('update-location', {
                lat, lon,
                gameKey: get(Game.store).game._key,
                userKey: get(userStore).key
            });
        } catch (err) {
            console.log(err);
        }
    }
    
    static async updateSettings(form) {
        try {
            Game.stopPolling();
            console.log({form})
            console.log(Game.game._key)
            Game.send('update-settings', {
                gameKey: Game.game._key,
                settings: form
            });
            const res = await new Promise((res, rej) => {
                Game.ws.onmessage = (m) => {
                    try {
                        console.log({m})
                        const { method, data } = JSON.parse(m.data);
                        if (method === 'update-game') {
                            Game.handleGameUpdate(data);
                            if (data?.game?.page === 'map') res()
                        }
                        else if (method === 'update-settings') {
                            Game.handleGameUpdate(data);
                            res()
                        }
                    } catch (e) {
                        rej(e);
                    }
                }
                Game.ws.onerror = rej;
            });
            Game.resumePolling();
            return true;
        } catch (err) {
            pushPopup(0, "Unable to update settings. Please try again.");
            return false;
        }
    }

    static updateTime(form) {
        try {
            const gameKey = get(Game.store).game._key;
            Game.send('update-time', { gameKey, settings: form });
        } catch (err) {
            console.log(err);
        }
    }

    static get players() {
        return get(Game.store)?.players || [];
    }
    static get player() {
        return get(Game.store)?.player;
    }
    static get destinations() {
        return get(Game.store)?.destinations || [];
    }
    static get game() {
        return get(Game.store)?.game;
    }
    static get nextDestination() {
        if (!Game.player || Game.player.destinationIndex >= Game.destinations.length) {
            return null;
        }
        return Game.destinations[Game.player.destinationIndex];
    }
    static get key() {
        return Game.game._key
    }
};