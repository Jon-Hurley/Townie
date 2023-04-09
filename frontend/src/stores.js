import { get, writable } from 'svelte/store';
import { logout } from './requests/account';

export const userStore = writable();

export const updateAccessToken = (res) => {
    const token = res?.data?.token;
    if (!token) return;
    console.log("NEW TOKEN:", token);
    userStore.set({ ...get(userStore), token });
};

export const popupQueue = writable([]);

export const pushPopup = (status, message, onOk) => {
    const cp = [ ...get(popupQueue) ];
    cp.push({
        status,
        message,
        onOk: () => {
            popPopup();
            if (onOk) onOk();
            if (message.includes('Invalid token')) {
                logout();
            }
        }
    })
    popupQueue.set(cp);
}

export const popPopup = () => {
    const queue = [ ...get(popupQueue) ];
    queue.shift(1);
    popupQueue.set(queue);
}