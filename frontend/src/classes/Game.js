import { writable, get } from 'svelte/store';
import { userStore } from '../stores.js';
import { PUBLIC_BACKEND_WS } from '$env/static/public';

export class Game {
    static store = writable();
    /** @type {WebSocket} */
    static ws = undefined;
    static interval = undefined;
    static messageObj = writable({
        status: 0,
        message: null,
        dest: null
    });

    static send(method, data) {
        const objStr = JSON.stringify({ method, ...data });
        Game.ws.send(objStr);
    }

    static setDefaultEvents() {
        Game.ws.onmessage = (m) => {
            try {
                var res = JSON.parse(m.data);
                console.log("WS MESSAGE:", res);
                
                switch (res.method) {
                    case 'get-game':
                    case 'update-game': {
                        Game.store.set(res.data);
                        return;
                    }
                    default: {
                        console.log("No response behavior")
                    }
                } 

            } catch (err) {
                console.log("WS ERROR:", m, err);
                Game.messageObj.set({
                    status: 0,
                    message: err,
                    dest: null
                });
                return;
            }        
        };
        Game.ws.onerror = (e) => {
            console.log("WS ERROR:", e);
            Game.messageObj.set({
                status: 0,
                message: err,
                dest: null
            });
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
            const userKey = get(userStore).key;
            Game.ws = new WebSocket(`${PUBLIC_BACKEND_WS}?gameKey=${gameKey}&userKey=${userKey}`);
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
        } catch (err) {
            console.log(err);
            Game.ws?.close();
            Game.ws = undefined;
            Game.store.set(null);
            Game.messageObj.set({
                status: 0,
                message: "Unable to connect to lobby. Please try again.",
                dest: null
            });
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
};