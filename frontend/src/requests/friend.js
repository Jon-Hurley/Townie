import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { userStore } from '../stores';

export const getFriends = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/friends/',
            {
                key: get(userStore).key
            }
        );
        console.log(res);
        return res.data.friends || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const sendFriendRequest = async(toKey, toPhone) => {
    let user = get(userStore);
    console.log(user);
    try {
        console.log(user.username);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/request-friend/',
            {
                username: get(userStore).username,
                toPhone: toPhone,
                fromKey: get(userStore).key,
                toKey: toKey
            }
        );
        return res.data.key;
        //return false;
    } catch (err) {
        console.log(err);
        return false;
    }
};

export const acceptFriend = async(friendshipKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/accept-friend/',
            {
                username: get(userStore).username,
                key: friendshipKey
            }
        );
        return true;
    } catch (err) {
        console.log({err});
        return false;
    }
};

// Deletes a friendship edge. User for:
//      canceling a friend request
//      removing a friend
//      reject a friend request
export const rejectFriend = async(friendshipKey) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/reject-friend/',
            {
                key: friendshipKey
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