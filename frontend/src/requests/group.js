import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';

export const createGame = async() => {
    try {
        const res = await axios.get(
            PUBLIC_BACKEND_API + 'group/create-game'
        );
        return res.data.key;
    } catch (err) {
        console.log(err);
        return null;
    }
};