import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { userStore } from '../stores';
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
                key: get(userStore).key,
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
            PUBLIC_BACKEND_API + 'group/get-summary/',
            {
                gameKey,
            }
        );
        return res.data;
    } catch (err) {
        console.log(err);
        return false;
    }
}

export const getGameLog = async () => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/game-log/',
            {
                key: get(userStore).key
            }
        );
        console.log(res.data);
        return res.data.games;
    } catch (err) {
        console.log(err);
        return null;
    }
}

export const submitRating = async (theme, rating, numRatings) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/submit-rating/',
            {
                theme,
                rating,
                numRatings,
            }
        );
        return res.data;
    } catch (err) {
        console.log(err);
        return false;
    }
}