import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { updateAccessToken, userStore } from '../stores';

export const createGame = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'group/create-game/', {
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
        return res.data.key;
    } catch (err) {
        const err_message = "Unable to create game. Please try again.";
        pushPopup(0, err_message);
        return false;
    }
};
