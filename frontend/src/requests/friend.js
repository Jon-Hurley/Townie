import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { updateAccessToken, userStore } from '../stores';

export const getFriends = async() => {
    try {
        const body = {
            key: get(userStore).key,
            token: get(userStore).token
        }
        console.log(body)
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/friends/',
            body
        );
        updateAccessToken(res);
        console.log(res);
        return res.data.friends || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const sendFriendRequest = async(toKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/request-friend/',
            {
                fromKey: get(userStore).key,
                toKey: toKey,
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
        console.log("res: ", res.data)
        return res.data;
    } catch (err) {
        console.log(err);
        return {errorMessage: "Unable to send friend request. Please try again."};
    }
};

export const acceptFriend = async(friendshipKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/accept-friend/',
            {
                key: friendshipKey,
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
        return null;
    } catch (err) {
        console.log(err);
        return "Unable to accept friend. Please try again.";
    }
};

// Deletes a friendship edge. User for:
//      canceling a friend request
//      removing a friend
//      reject a friend request
export const rejectFriend = async(friendshipKey) => {
    try {
        const body = {
            key: friendshipKey,
            token: get(userStore).token
        };
        console.log(body)
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/reject-friend/',
            body
        );
        updateAccessToken(res);
        return null;
    } catch (err) {
        console.log(err);
        return "Unable to remove or reject friend. Please try again.";
    }
};

const processPending = (pendingRes) => {  
    const pendingList = pendingRes?.data?.pending || [];
    console.log({pendingList})
    pendingList.forEach(
        x => {
            x.title = x.inbound ? 'Incoming Friend Request'
                                : 'Outgoing Friend Request'
        }
    );
    return pendingList;
};

export const loadNotifications = async() => {
    try {
        const [ pendingRes ] = await Promise.all([
            axios.post(
                PUBLIC_BACKEND_API + 'user/pending-friends/',
                {
                    key: get(userStore).key,
                    token: get(userStore).token
                }
            )
        ]);
        updateAccessToken(res);
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