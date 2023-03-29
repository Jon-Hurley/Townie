import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { userStore } from '../stores';
import { get } from 'svelte/store';

export const getUsers = async(substr) => {
    if (!substr || substr.length === 0) {
        return [];
    }
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/search/',
            {
                substr
            }
        );
        return res.data.users || [];
    } catch (e) {
        console.log(e);
        return [];
    }
};

export const getUser = async(targetKey) => {
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

export const getGameLog = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/gameLog/',
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