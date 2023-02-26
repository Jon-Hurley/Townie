import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { userStore } from '../stores';

export const login = async(username, password) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/account/',
            {
                password: password,
                username: username
            }
        );
        data = json.loads(res.body);
        success = data.get('success');
        if (success == false) {
            return false;
        }
        username = data.get('username');
        key = data.get('key');
        phone = data.get('phone');
        points = data.get('points');
        purchases = data.get('purchases')
        rank = data.get('rank');

        userStore.set(username + "/" + key, key, passwordHash, phone, points, purchases, rank);
        console.log(res);
        return true;        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const signup = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/account/',
            {
                key: get(userStore).key
            }
        );
        console.log(res);
        return res.data.account || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const verification = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/account/',
            {
                key: get(userStore).key
            }
        );
        console.log(res);
        return res.data.account || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const loginWithToken = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/account/',
            {
                key: get(userStore).key
            }
        );
        console.log(res);
        return res.data.account || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const initiatePasswordReset = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/account/',
            {
                key: get(userStore).key
            }
        );
        console.log(res);
        return res.data.account || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};

export const completePasswordReset = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/account/',
            {
                key: get(userStore).key
            }
        );
        console.log(res);
        return res.data.account || [];        
    } catch (err) {
        console.log(err);
        return [];
    }
};