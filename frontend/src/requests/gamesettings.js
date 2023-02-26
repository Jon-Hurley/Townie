import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { userStore } from '../stores';

export const sendPreferences = async() => {
    try {
        const res = await axios.post(
                PUBLIC_BACKEND_API + 'group/scraper/',
                {
                    lat: 40.423538,
                    lng: -86.921738,
                    radius: '50',
                    theme: 'restaurant',
                    transportation: 'car',
                }
        );
        console.log(res);
        return res.data.destinations || [];
    } catch (err) {
        console.log(err)
        return [];

    }
}