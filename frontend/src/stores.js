import { writable } from 'svelte/store';
import { PUBLIC_BACKEND_WS } from '$env/static/public';

export const groupStore = writable();
export const userStore = writable();

export const logout = () => {

}

export const login = () => {

}

export const autoLogin = () => {

}

export const signin = () => {

}

let ws;

export const joinLobby = () => {
    ws = new WebSocket(PUBLIC_BACKEND_WS)
    console.log(ws)
}