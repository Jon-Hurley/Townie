import * as turf from '@turf/turf';

import { writable, get } from 'svelte/store';
import { PUBLIC_BACKEND_WS } from '$env/static/public';
import { goto } from '$app/navigation';

import { pushPopup, userStore } from '../stores.js';
import { Location } from './Location.js';

import { Map } from './Map.js';

export class Game {
    static store = writable();
    /** @type {WebSocket} */
    static ws = undefined;
    static interval = undefined;
    static timeStore = writable(null);
    static messageStore = writable([]);
    static formatStore = writable("");
    static distanceStore = writable(0);

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

    static updateDistance() {
        const currLat = Location.lat;
        const currLng = Location.lng;
        const destLat = Game.nextDestination.lat;
        const destLng = Game.nextDestination.lon;
        const from = turf.point([currLng, currLat]);
        const to = turf.point([destLng, destLat]);
        let distance = turf.distance(from, to, {units: 'miles'}); 
        return Math.round(distance);
    }

    static handleGameUpdate(data) {
        if (!data) return;
        data.destinations.sort((a, b) => a.index - b.index);

        console.log("SETTING GAME STORE")
        Game.store.set(data);
    }

    // TODO: continue experimenting with this
    static shrinkRadius() {
        console.log("SHRINKING RADIUS")
        const startTime = Date.now();
        const timeLeft = Game?.nextDestination?.timeToCompletion * 1000;
        let timeComputation = -1;
        let currTime = startTime;
        let interval = setInterval(() => {
            currTime += timeLeft / 5.0;
            if (get(Map.settings).destinationRadius * get(Map.settings).destinationRadiusScalar < 0.1 || get(Game.timeStore)) {
                clearInterval(interval);
            }
            if (currTime > (timeLeft + startTime)) {
                timeComputation = (currTime - startTime) / timeLeft;
            }
            if (timeComputation < 1.2 && timeComputation > 1) {
                Map.updateDestinationRadiusScalar(x => x * 0.85);
                pushPopup({
                    status: 3,
                    message: `You are running out of time! Hurry up!\n
                    The destination radius is now 85% of its original size.`,
                    onOk: () => {}
                });
            }
            else if (timeComputation < 1.4 && timeComputation > 1) {
                Map.updateDestinationRadiusScalar(x => x * 0.70);
                pushPopup({
                    status: 3,
                    message: `You are running out of time! Hurry up!\n
                    The destination radius is now 70% of its original size.`,
                    onOk: () => {}
                });
            }
            else if (timeComputation < 1.6 && timeComputation > 1) {
                Map.updateDestinationRadiusScalar(x => x * 0.55);
                pushPopup({
                    status: 3,
                    message: `You are running out of time! Hurry up!\n
                    The destination radius is now 55% of its original size.`,
                    onOk: () => {}
                });
            }
            else if (timeComputation < 1.8 && timeComputation > 1) {
                Map.updateDestinationRadiusScalar(x => x * 0.40);
                pushPopup({
                    status: 3,
                    message: `You are running out of time! Hurry up!\n
                    The destination radius is now 40% of its original size.`,
                    onOk: () => {}
                });
            }
            else if (timeComputation < 2 && timeComputation > 1) {
                Map.updateDestinationRadiusScalar(x => x * 0.15);
                pushPopup({
                    status: 3,
                    message: `You are running out of time! Hurry up!\n
                    The destination radius is now 15% of its original size.`,
                    onOk: () => {}
                });
            }
            else if  (timeComputation > 2) {
                Map.updateDestinationRadiusScalar(x => x = 0);
                Map.updateDestinationCircle();
                pushPopup({
                    status: 3,
                    message: `You are out of time! This destination is now worth zero points.\n
                    You can still visit it, but you will not receive any points.\n
                    Luckily, you now have its exact location!`,
                    onOk: () => {}
                });
                clearInterval(interval);
            }
            
            Map.updateDestinationCircle();
        }, timeLeft / 5.0);
    }

    static handleRadiusUpdate() {
        const currLat = Location.lat;
        const currLng = Location.lng;

        const destLat = Game.nextDestination.lat;
        const destLng = Game.nextDestination.lon;

        const from = turf.point([currLng, currLat]);
        const to = turf.point([destLng, destLat]);
        let distance = turf.distance(from, to, {units: 'kilometers'}) / 2.0;

        Map.updateDestinationRadius(x => x = distance);
    }

    static handleLocationUpdate(data) {
        console.log("LOCATION UPDATE:", data);
        if (!data) return;

        const {
            newTime, newDist, oldTime, oldDist,
            totalTime, totalDist,
            arrived, atPrevDest,
            potentialPoints, points,
            achievedDest
        } = data;

        if (get(Game.timeStore) != atPrevDest) {
            Game.timeStore.set(atPrevDest)
        }

        if (arrived) {
            const displayTime = Math.round(10 * oldTime / (1000 * 60)) / 10;
            const displayDist = Math.round(oldDist / 100) / 10;
           
            // open destination page.
            const baseUrl = window.location.protocol + "//" + window.location.host + "/";
            console.log({achievedDest});
            localStorage.setItem('lastPage', '/app/destination/' + achievedDest._key);
            window.open(baseUrl + 'app/destination/' + achievedDest._key, '_blank');

            pushPopup({
                status: 1,
                message: `
                    You reached destination: ${achievedDest.name}!\n
                    You took ${displayTime} minutes and traveled ${displayDist} km.\n
                    You received ${potentialPoints}/${points} points.\n
                    Your total time has been paused and will resume once you leave the destination.
                `,
                onOk: () => {
                    Game.player.destinationIndex++;
                    Game.formatStore.set(Game.updateDestTime());
                }
            });

            if (achievedDest.index === Game.destinations.length - 1) {
                pushPopup({
                    status: 1,
                    message: "You have reached the final destination. You won the game!",
                    onOk: () => Game.leave()
                });
            }
        }
    }

    static updateDestTime() {
        const totalTime = Game.nextDestination.timeToCompletion;

        const dHours = `00${Math.floor((totalTime / 60 / 60) % 60)}`.slice(-2);
        const dMinutes = `00${Math.floor((totalTime / 60) % 60)}`.slice(-2);
        const dSeconds = `00${Math.floor((totalTime) % 60)}`.slice(-2);

        let formattedTime = "";

        if (dHours !== '00')
            formattedTime = `${dHours}:${dMinutes}:${dSeconds}`;
        else if (dHours === '00' && dMinutes !== '00')
            formattedTime = `${dMinutes}:${dSeconds}`;
        else if (dHours === '00' && dMinutes === '00')
            formattedTime = `${dSeconds} seconds`;

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
                        Game.handleRadiusUpdate();
                        Game.distanceStore.set(Game.updateDistance());
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
                pushPopup({
                    status: 0,
                    message: "Connections error. Please try again later."
                });
            }
        };
        Game.ws.onerror = (e) => {
            console.log("WS ERROR:", e);
            pushPopup({
                status: 0,
                message: "Connections error. Please try again later."
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

        // Game.interval = setInterval(() => {
        //     if (get(Game?.store)?.game) {
        //         Game.send('get-game', {
        //             gameKey: get(Game.store).game._key
        //         });
        //     }
        // }, 10000);
    }

    static stopPolling() {
        // clearInterval(Game.interval);
        // Game.interval = undefined;
    }

    static async getGame(gameKey) {
        Game.stopPolling();

        Game.send('get-game', { gameKey });
        const res = await new Promise((res, rej) => { 
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

        Game.resumePolling();
        return res;
    }

    static async join(gameKey) {
        try {
            Game.messageStore.set([]);

            const userLocation = await Location.getCurrentLocation();
            Location.store.set(userLocation);
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

            if (!Game.ws) {
                throw { message: "Unable to create websocket. Try again." }
            }

            const res = await Game.getGame(gameKey);
            if (!res?.player) {
                throw { message: "Unable to connect to game. Your session token may be expired." }
            }
            
            return true;
        } catch (err) {
            console.log(err);
            Game.ws?.close();
            Game.ws = undefined;
            Game.store.set(undefined);
            pushPopup({
                status: 0,
                message: err?.message || "Unable to connect to lobby. Please try again."
            });
            return false;
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
                        console.log({ m })
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
             // TODO: continue experimenting with this
            Game.shrinkRadius();
            return true;
        } catch (err) {
            pushPopup({
                status: 0,
                message: "Unable to start game. Please try again. You may need to change your settings.",
                onOk: () => Game.resumePolling()
            });
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
            console.log({ form })
            console.log(Game.game._key)
            Game.send('update-settings', {
                gameKey: Game.game._key,
                settings: form
            });
            const res = await new Promise((res, rej) => {
                Game.ws.onmessage = (m) => {
                    try {
                        console.log({ m })
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
            pushPopup({
                status: 0,
                message: "Unable to update settings. Please try again.",
                onOk: () => Game.resumePolling()
            });
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