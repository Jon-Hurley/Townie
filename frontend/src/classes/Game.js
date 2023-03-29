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
            try {
                const res = JSON.parse(m.data);
                console.log("WS MESSAGE:", res);
                switch (res.method) {
                    case 'get-game':
                    case 'update-game': {
                        res.data.destinations.sort((a, b) => a.index - b.index);
                        Game.store.set(res.data);

                        if (Map.map) {

                            console.log("We zoomin")
    
                            Map.generateUserMarker();
                            Map.generateDestinationCircle();
                            Map.generatePlayerMarkers();
    
                            Map.setZoomAndCenter();
                        }
                        return;
                    }
                    case 'update-location': {
                        console.log(res.data);
                        const {
                            destinationIndex, reached, quiet,
                            time,
                            dist,
                            totalTime,
                            totalDist
                        } = res.data;
                        if (!quiet && reached) {
                            const achievedDest = get(Game.store).destinations[destinationIndex];
                            pushPopup(
                                0,
                                `You reached destination ${achievedDest.n}!\n
                                You took ${time} minutes and traveled ${dist} miles.\n
                                Total time: ${totalTime} minutes\n
                                Total distance: ${totalDist} miles`
                            );
                            if (destinationIndex === get(Game.store).destinations.length - 1) {
                                Game.leave();
                                pushPopup(0, "You won!");
                            }
                        }
                    }
                    default: {
                        console.log("No response behavior")
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
            const userKey = get(userStore).key;
            Game.ws = new WebSocket(`${PUBLIC_BACKEND_WS}?gameKey=${gameKey}&userKey=${userKey}`);
            await new Promise((res, rej) => { 
                Game.ws.onerror = () => rej();
                Game.ws.onopen = (e) => res(e);
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
            console.log(res)
            // res.player

            Game.store.set(res);

            Game.setDefaultEvents();
        } catch (err) {
            console.log(err);
            Game.ws?.close();
            Game.ws = undefined;
            Game.store.set(null);
            pushPopup(0, "Unable to connect to lobby. Please try again.");
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

    static updateTime(form) {
        try {
            const gameKey = get(Game.store).game._key;
            Game.send('update-time', { gameKey, settings: form});
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