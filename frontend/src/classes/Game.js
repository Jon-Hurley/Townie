import { writable, get } from 'svelte/store';
import { pushPopup, userStore } from '../stores.js';
import { PUBLIC_BACKEND_WS } from '$env/static/public';
import { Map } from './Map.js';
import { Location } from './Location.js';
import { goto } from '$app/navigation';
import { logout } from '../requests/account.js';
import * as turf from '@turf/turf';

export class Game {
    static store = writable();
    /** @type {WebSocket} */
    static ws = undefined;
    static interval = undefined;
    static timeStore = writable(null);
    static messageStore = writable([]);
    static formatStore = writable("");

    static send(method, data) {
        const objStr = JSON.stringify({ method, ...data });
        Game.ws.send(objStr);
    }

    static handleNewMessage(data) {
        Game.messageStore.set([
            ...get(Game.messageStore),
            data
        ]);
    }

    static handleGameUpdate(data) {
        if (!data) return;
        data.destinations.sort((a, b) => a.index - b.index);    
        Game.store.set(data);
    }

    static handleRadiusUpdate(data) {
        const {
            newTime, newDist, oldTime, oldDist,
            totalTime, totalDist,
            arrived, atPrevDest,
            potentialPoints, points
        } = data;

        const currLat = Location.lat;
        const currLng = Location.lng;

        const destLat = Game.nextDestination.lat;
        const destLng = Game.nextDestination.lon;

        const from = turf.point([currLng, currLat]);
        const to = turf.point([destLng, destLat]);
        let distance = turf.distance(from, to, {units: 'kilometers'}) / 2.0;
        const startTime = Game?.game?.createTime;
        const currTime = newTime;
        const timeLeft = Game?.nextDestination?.timeToCompletion * 1000;
        const radius = get(Map.settings).destinationRadius;
        let timeComputation = -1;
        if (currTime > timeLeft) {
            timeComputation = currTime / timeLeft;
        }
        if (timeComputation < 1.2 && timeComputation > 1) {
            distance = distance / 1.2;
        }
        else if (timeComputation < 1.4 && timeComputation > 1) {
            distance = distance / 1.4;
        }
        else if (timeComputation < 1.6 && timeComputation > 1) {
            distance = distance / 1.6;
        }
        else if (timeComputation < 1.8 && timeComputation > 1) {
            distance = distance / 1.8;
        }
        else if (timeComputation < 2 && timeComputation > 1) {
            distance = distance / 2.0;
        }
        else if  (timeComputation > 2) {
            distance = 0;
        }


        Map.updateDestinationRadius(x => x = distance);
    }

    static handleLocationUpdate(data) {
        console.log("LOCATION UPDATE:", data);
        if (!data) return;

        const {
            newTime, newDist, oldTime, oldDist,
            totalTime, totalDist,
            arrived, atPrevDest,
            potentialPoints, points
        } = data;
        
        if (get(Game.timeStore) != atPrevDest) {
            Game.timeStore.set(atPrevDest)
        }

        if (arrived) {
            const achievedDest = Game.nextDestination;
            const displayTime = Math.round(10 * oldTime / (1000 * 60)) / 10;
            const displayDist = Math.round(oldDist / 100) / 10;
           
            pushPopup(
                1,
                `You reached destination: ${achievedDest.name}!\n
                You took ${displayTime} minutes and traveled ${displayDist} km.\n
                You received ${potentialPoints}/${points} points.\n
                Your total time has been paused and will resume once you leave the destination.`,
                () => {
                    Game.player.destinationIndex++;
                    Game.formatStore.set(Game.updateDestTime());
                }
            );
            if (achievedDest.index === Game.destinations.length - 1) {
                pushPopup(
                    1, "You have reached the final destination. You won the game!",
                    () => Game.leave()
                );
            }
        }
    }

    static updateDestTime() {
        const totalTime = Game.nextDestination.timeToCompletion;
        const gHours = `00${Math.floor((totalTime / 60 / 60) % 60)}`.slice(-2);
        const gMinutes = `00${Math.floor((totalTime / 60) % 60)}`.slice(-2);
        const gSeconds = `00${Math.floor((totalTime) % 60)}`.slice(-2);
        let formattedTime = "";
        if (gHours !== '00')
            formattedTime = `${gHours}:${gMinutes}:${gSeconds}`;
        else if (gHours === '00' && gMinutes !== '00')
            formattedTime = `${gMinutes}:${gSeconds}`;
        else if (gHours === '00' && gMinutes === '00')
            formattedTime = `${gSeconds} seconds`;

        return formattedTime;
    }

    static setDefaultEvents() {
        Game.ws.onmessage = (m) => {
            try {
                const { method, data } = JSON.parse(m.data);
                console.log("WS MESSAGE:", { method, data });
                switch (method) {
                    case 'get-game':
                    case 'update-game': {
                        Game.handleGameUpdate(data);  
                        return;
                    }
                    case 'update-location': {
                        Game.handleLocationUpdate(data);
                        Game.handleRadiusUpdate(data);
                        return;
                    }
                    case 'new-message': {
                        Game.handleNewMessage(data); return;
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

    static async getGame(gameKey) {
        Game.send('get-game', { gameKey });
        return await new Promise((res, rej) => { 
            Game.ws.onerror = () => rej();
            Game.ws.onmessage = (m) => {
                try {
                    const { method, data } = JSON.parse(m.data);
                    if (method !== 'get-game') return;
                    if (!data?.game?._key) rej();
                    Game.handleGameUpdate(data);
                    res(data);
                } catch (e) {
                    console.log(e)
                    rej({message: 'Invalid game key. Please try again.'});
                }
            };
        });
    }

    static async join(gameKey) {
        try {
            Game.messageStore.set([]);

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
                Game.ws.onerror = () => rej({ message: 'Unable to connect to web-socket.' });
                Game.ws.onopen = (e) => res(e);
            });

            const res = await Game.getGame(gameKey);
            if (!res?.player) {
                throw { message: "Unable to connect to game. Your session token may be expired." }
            }

            Game.store.set(res);
            Game.resumePolling();
        } catch (err) {
            console.log(err);
            Game.ws?.close();
            Game.ws = undefined;
            Game.store.set(null);
            pushPopup(0,
                err?.message || "Unable to connect to lobby. Please try again."
            );
        }
    }

    static leave() {
        try {
            Game.stopPolling();
            Game.ws?.close();
            Game.ws = undefined;
            goto('/app/game-summary/' + Game.key);
            Game.messageStore.set([]);
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
            pushPopup(
                0, "Unable to start game. You may have to change your settings.",
                () => Game.resumePolling()
            );
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
            pushPopup(
                0, "Unable to update settings. Please try again.",
                () => Game.resumePolling()
            );
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
        return Game.game?._key
    }
};