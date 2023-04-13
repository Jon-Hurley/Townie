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

// OPTIONS:
// status,
// message,
// onOk,
// onCancel,
// cancelText = 'Cancel',
// okText = 'Ok',
// includeCancel = false

export const pushPopup = (popupObject) => {
    const cp = [ ...get(popupQueue) ];
    cp.push({
        ...popupObject,
        onOk: () => {
            popPopup();
            if (popupObject.onOk) onOk();
            if (message.includes('Invalid token')) {
                logout();
            }
        },
        onCancel: () => {
            popPopup();
            if (popupObject.onCancel) onCancel();
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