import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { pushPopup, updateAccessToken, userStore } from '../stores';

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
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to remove or reject friend. Please try again.";
        pushPopup({status: 0, message: err_message});
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
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to send friend request. Please try again.";
        pushPopup({status: 0, message: err_message});
        return false;
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
        return true;
    } catch (err) {
        console.log(err);
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to accept friend. Please try again.";
        pushPopup({status: 0, message: err_message});
        return false;
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
        return true;
    } catch (err) {
        console.log(err);
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to remove or reject friend. Please try again.";
        pushPopup({status: 0, message: err_message});
        return false;
    }
};

const processPending = (pendingRes) => {  
    const pendingList = pendingRes?.value?.data?.pending || [];
    console.log({pendingList})
    pendingList.forEach(
        x => {
            x.title = x.inbound ? 'Incoming Friend Request'
                                : 'Outgoing Friend Request'
        }
    );
    return pendingList;
};

const processPendingUsersInGame = (onlineRes) => {  
    const pendingList = onlineRes?.value?.data?.onlinePlayers || [];
    console.log({pendingList})
    pendingList.forEach(
        x => {
            x.title = 'Your friend is in a game'
        }
    );
    return pendingList;
};

export const loadNotifications = async() => {
    try {
        const [ pendingRes, onlinePlayerRes ] = await Promise.allSettled(
            [
                axios.post(
                    PUBLIC_BACKEND_API + 'user/pending-friends/',
                    {
                        token: get(userStore).token
                    }
                ),
                axios.post(
                    PUBLIC_BACKEND_API + 'user/online-users/',
                    {
                        key: get(userStore).key,
                        token: get(userStore).token
                    }
                )
            ]
        );
        updateAccessToken(pendingRes);

        const notifs = [
            ...processPending(pendingRes),
            ...processPendingUsersInGame(onlinePlayerRes)
        ];
        notifs.sort((a, b) => b.timestamp - a.timestamp);
        
        return notifs;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to remove or reject friend. Please try again.";
        pushPopup({status: 0, message: err_message});
        return [];
    }
};

export const loadFriendsInGameNotifs = async() => {
    try {
        const [ pendingRes ] = await Promise.all([
            axios.post(
                PUBLIC_BACKEND_API + 'user/friends-game/',
                {
                    key: get(userStore).key,
                    token: get(userStore).token
                }
            )
        ]);
        updateAccessToken(pendingRes);

        const notifs = [
            ...processPendingGame(pendingRes)
        ];
        notifs.sort((a, b) => b.timestamp - a.timestamp);
        
        return notifs;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to remove or reject friend. Please try again.";
        pushPopup({status: 0, message: err_message});
        return [];
    }
};