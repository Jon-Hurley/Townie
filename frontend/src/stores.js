import { get, writable } from 'svelte/store';
import { logout } from './requests/account';

export const userStore = writable();

export const updateAccessToken = (res) => {
    const token = res?.data?.token;
    if (!token) return;
    console.log("NEW TOKEN:", token);
    userStore.set({ ...get(userStore), token });
};

export const primaryColor = writable('indigo');
export const primaryAudio = writable(null);

export const handlePurchaseUpdates = (user) => {
    if (!user) return;
    
    let newPrimaryColor = 'indigo';
    let newPrimaryAudio = null;

    for (const p of user.purchases) {
        if (!p?.isActive) continue;
        switch (p.category) {
            case 'Color': {
                newPrimaryColor = p.name.toLowerCase();
                break;
            }
            case 'Music': {
                newPrimaryAudio = p.name;
                break;
            }
            default: {
                console.log("Unrecognized purchase category:", p.category);
            }
        }
    }

    if (get(primaryColor) !== newPrimaryColor)
        primaryColor.set(newPrimaryColor);
    if (get(primaryAudio) !== newPrimaryAudio)
        primaryAudio.set(newPrimaryAudio);
}

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
            if (popupObject.onOk) popupObject.onOk();
            if (popupObject.message.includes('Invalid token')) {
                logout();
            }
        },
        onCancel: () => {
            popPopup();
            if (popupObject.onCancel) popupObject.onCancel();
            if (popupObject.message.includes('Invalid token')) {
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