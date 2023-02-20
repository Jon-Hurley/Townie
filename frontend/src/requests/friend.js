import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { userStore } from '../stores';

export const getFriends = async(key) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/friends/',
            {
                key
            }
        );
        console.log(res);
        return res.data.friends || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const acceptFriend = async(key) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/accept-friend/',
            {
                key
            }
        );
        return true;
    } catch (err) {
        console.log(err);
        return false;
    }
};

export const rejectFriend = async(key) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/reject-friend/',
            {
                key
            }
        );
        return true;
    } catch (err) {
        console.log(err);
        return false;
    }
};

const processPending = (pendingRes) => {
    const pendingList = pendingRes?.data?.pending || [];
    pendingList.forEach(
        x => x.title = 'Incoming Friend Request'
    );
    return pendingList;
};

export const loadNotifications = async() => {
    try {
        const [ pendingRes ] = await Promise.all([
            axios.post(
                PUBLIC_BACKEND_API + 'user/pending-friends/',
                {
                    key: get(userStore).key
                }
            )
        ]);
        const notifs = [
            ...processPending(pendingRes)
        ];
        notifs.sort((a, b) => b.timestamp - a.timestamp);
        return notifs;
    } catch (err) {
        console.log(err);
        return [];
    }
};