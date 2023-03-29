import { get, writable } from 'svelte/store';
import { logout } from './requests/account';

export const userStore = writable();

export const mapStore = writable();

export const gamePage = writable('/game/join');

export const updateAccessToken = (res) => {
    const token = res?.data?.token;
    if (!token) return;
    console.log("NEW TOKEN:", token);
    userStore.set({ ...get(userStore), token });
};

export const popupQueue = writable([]);

export const pushPopup = (status, message, onOk) => {
    popupQueue.set([
        ...get(popupQueue),
        {
            status,
            message,
            onOk: () => {
                const queue = [ ...get(popupQueue) ];
                queue.shift(1);
                popupQueue.set(queue);
                console.log({queue});
                if (onOk) onOk();
            }
        }
    ]);
}