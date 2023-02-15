import { writable } from 'svelte/store';
import { PUBLIC_BACKEND_WS } from '$env/static/public';

export const groupStore = writable();
export const userStore = writable();

let ws;

export const login = () => {
    ws = new WebSocket(PUBLIC_BACKEND_WS)
    console.log(ws)
}
