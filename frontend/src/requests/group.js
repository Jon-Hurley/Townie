import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { pushPopup, updateAccessToken, userStore } from '../stores';
import { Location } from '../classes/Location';
import { Game } from '../classes/Game';

export const createGame = async() => {
    try {
        const loc = await Location.getCurrentLocation();
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'group/create-game/', {
                token: get(userStore).token,
                lat: loc.lat,
                lon: loc.lng
            }
        );
        updateAccessToken(res);
        return res.data.key;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to create game. Please try again.";
        pushPopup({status: 0, message: err_message});
        return false;
    }
};

export const getThemeList = async() => {
    try {
        const res = await axios.get(
            PUBLIC_BACKEND_API + 'group/get-theme-list/'
        );
        return res.data;
    } catch (err) {
        console.log(err);
        return null;
    }
};
