import { writable } from 'svelte/store';
import { logout } from './requests/account';

export const userStore = writable();

export const mapStore = writable();

export const gamePage = writable('/game/join');

export const updateAccessToken = (res) => {
    if (!res?.data?.token) {
        return;
    }
    console.log("NEW TOKEN:", res.data.token);
    userStore.set({
        ...userStore,
        token: data.token
    });
};