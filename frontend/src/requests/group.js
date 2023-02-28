import axios from 'axios';
import { PUBLIC_BACKEND_API, PUBLIC_BACKEND_WS } from '$env/static/public';
import { gameStore, userStore } from '../stores';
import { get } from 'svelte/store';

export const createGame = async() => {
    try {
        const res = await axios.get(
            PUBLIC_BACKEND_API + 'group/create-game'
        );
        return res.data.key;
    } catch (err) {
        console.log(err);
        return null;
    }
};

/** @type {WebSocket} */
export let ws;

export const joinGame = async(gameKey) => {
    try {
        const userKey = get(userStore).key;
        ws = new WebSocket(
            `${PUBLIC_BACKEND_WS}?gameKey=${gameKey}&userKey=${userKey}`
        );
        const res = await new Promise((res, rej) => { 
            ws.onerror = () => rej();
            ws.onopen = () => res();
        });

        const data = await new Promise((res, rej) => {
            ws.onerror = () => rej();
            ws.onmessage = (m) => {
                const gameData = JSON.parse(m.data);
                console.log("WS MESSAGE:", gameData);
                gameStore.set(gameData);
                res();
            };
            const objStr = JSON.stringify({
                method: 'get-game',
                gameKey
            });
            ws.send(objStr);
        });
        setDefaultEvents();

        return true;
    } catch (err) {
        console.log(err);
        ws?.close();
        return false;
    }
};

export const leaveGame = async() => {
    try {
        stopPolling();
        gameStore.set(null);
        ws?.close();
        return true;
    } catch (err) {
        console.log(err);
        return false;
    }
};

export const startGame = async() => {
    try {
        const gameKey = get(gameStore).game._key;
        const objStr = JSON.stringify({
            method: 'start-game',
            gameKey
        });
        ws.send(objStr);
        resumePolling();
    } catch (err) {
        console.log(err);
    }
};

export const awardPoints = async(destinationIndex) => {
    try {
        const gameKey = get(gameStore).game._key;
        const objStr = JSON.stringify({
            method: 'award-points',
            gameKey,
            destinationIndex
        });
        ws.send(objStr);
    } catch (err) {
        console.log(err);
    }
};

export const updateLocation = async(lon, lat) => {
    try {
        const objStr = JSON.stringify({
            method: 'update-location',
            lon,
            lat
        });
        ws.send(objStr);
    } catch (err) {
        console.log(err);
    }
};

export const updateSettings = async(field, value) => {
    try {
        const objStr = JSON.stringify({
            method: 'update-settings',
            field,
            value
        });
        ws.send(objStr);
    } catch (err) {
        console.log(err);
    }
};

let interval;

export const setDefaultEvents = () => {
    ws.onmessage = (m) => {
        console.log("REMOTE UPDATE: ", m.data)
        const gameData = JSON.parse(m.data);
        console.log("WS MESSAGE:", gameData);
        gameStore.set(gameData);
    };
    ws.onerror = (e) => {
        console.log("WS ERROR:", e);
    }
}

export const resumePolling = () => {
    setDefaultEvents();
    stopPolling();
    const objStr = JSON.stringify({
        method: 'get-game',
        gameKey
    });
    interval = setInterval(() => {
        ws.send(objStr)
    }, 10000);
}

export const stopPolling = () => {
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
}