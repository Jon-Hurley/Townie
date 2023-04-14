import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { pushPopup, updateAccessToken, userStore } from '../stores';
import { get } from 'svelte/store';

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

export const getPurchases = async () => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/purchases/',
            {
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
        console.log(res.data)
        return res.data.purchases;
    } catch (err) {
        console.log(err);
        const errMessage = err?.response?.data?.errorMessage
                            || "Unable to retrive purchasables. Please try again.";
        pushPopup({ status: 0, message: errMessage })
        return [];
    }
}