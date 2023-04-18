import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { pushPopup, updateAccessToken, userStore } from '../stores';
import { get } from 'svelte/store';

// NOTE: ALL REQUESTS HERE SHOULD BE PUBLIC (NOT AUTH NEEDED).

export const getUsers = async (substr) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/search/',
            {
                substr,
                key: get(userStore).key
            }
        );
        return res.data.users || [];
    } catch (e) {
        console.log(e);
        return [];
    }
};

export const getUser = async (targetKey) => {
    try {
        console.log(get(userStore));
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/profile/' + targetKey + '/',
            {
                key: get(userStore).key, // Note: here non-token key passing is fine since getUser since information is not sensitive.
                targetKey: targetKey
            }
        );
        return res.data;
    } catch (err) {
        console.log(err);
        return null;
    }
};

export const getSummary = async (gameKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/get-summary/',
            {
                gameKey,
                token: get(userStore)?.token || undefined
            }
        );
        updateAccessToken(res);
        return res.data.summary;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Unable to retrieve game data. Please try again.';
        pushPopup({status: 0, message: err_message});
        return false;
    }
}

export const getDestination = async (destKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/get-destination/',
            {
                destKey,
                token: get(userStore)?.token || undefined
            }
        );
        updateAccessToken(res);
        return res.data.summary;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to retrieve destination data. Please try again.';
        pushPopup({status: 0, message: err_message});
        return false;
    }
}

export const getGameLog = async (targetKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/game-log/',
            {
                key: targetKey
            }
        );
        console.log(res.data);
        return res.data.games;
    } catch (err) {
        console.log(err);
        return null;
    }
}

export const getThemeList = async() => {
    try {
        const res = await axios.get(
            PUBLIC_BACKEND_API + 'user/get-theme-list/'
        );
        return res.data;
    } catch (err) {
        console.log(err);
        return null;
    }
}

export const incrementDestinationIndex = async (connectionID) => {
    // This is used to increment destination index for the case of skipping a destination.
    // I don't know if there's a better way but this works -- Jack
    const res = await axios.post(
        PUBLIC_BACKEND_API + "user/increment-index/",
        {
            connectionID
        }
    );
}