import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { pushPopup, updateAccessToken, userStore } from '../stores';
import { get } from 'svelte/store';

export const initiatePremiumSession = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/initiate-subscription/',
            {
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
        const url = res.data.url;
        const winder = window.open(url, '_blank');
        if (winder?.focus) winder.focus();
    } catch (err) {
        console.log(err)
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to process payments at this time. Please try again later.";
        pushPopup({status: 0, message: err_message});
    }
}

export const cancelPremium = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/cancel-subscription/',
            {
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
    } catch (err) {
        console.log(err)
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to process cancelation at this time. Please contact customer support at (123)456-7890.";
        pushPopup({status: 0, message: err_message});
    }
}

export const makePurchase = async (purchasableKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/purchase/',
            {
                token: get(userStore).token,
                purchasableKey,
            }
        );
        updateAccessToken(res);
        console.log(res.data);
        userStore.set(res.data);
        return true;
    } catch (err) {
        console.log(err);
        const errMessage = err?.response?.data?.errorMessage
                            || "Unable to make purchase. Please try again.";
        pushPopup({ status: 0, message: errMessage })
        return false;
    }
}

export const getPurchasables = async () => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/purchasables/',
            {
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
        console.log(res.data)
        return res.data.purchasables;
    } catch (err) {
        console.log(err);
        const errMessage = err?.response?.data?.errorMessage
                            || "Unable to retrive purchasables. Please try again.";
        pushPopup({ status: 0, message: errMessage })
        return [];
    }
}

export const activatePurchase = async (purchasableKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/activate-purchase/',
            {
                token: get(userStore).token,
                purchasableKey
            }
        );
        updateAccessToken(res);
        userStore.set(res.data);
        return true;
    } catch (err) {
        console.log(err);
        const errMessage = err?.response?.data?.errorMessage
                            || "Unable to activate purchase. Please try again.";
        pushPopup({ status: 0, message: errMessage })
        return [];
    }
}