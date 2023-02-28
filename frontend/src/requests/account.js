import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { userStore } from '../stores';

export const login = async(username, password) => {
    console.log("HERE")
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/login/',
            {
                password: password,
                username: username
            }
        );
        console.log(res)
//        data = res.data
//        success = data.success;
//        if (success == false) {
//            return false;
//        }
//        username = data.username;
//        key = data.key;
//        phone = data.phoneNumber;
//        points = data.points;
//        purchases = data.purchases;
//        rank = data.rank;
//
//        userStore.set(username + "/" + key, key, passwordHash, phone, points, purchases, rank);
//        console.log(res);
        return true;        
    } catch (err) {
        console.log(err);
        return false;
    }
};

export const signup = async(username, password, phoneNumber) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/signup/',
            {
                username: username,
                password: password,
                phoneNumber: phoneNumber
            }
        );
        
        data = JSON.parse(res);
        success = data.success;
        if (success == false) {
            return false;
        }

        username = data.username;
        key = data.key;
        phone = data.phoneNumber;
        points = data.points;
        purchases = data.purchases;
        rank = data.rank;
        token = Math.floor(Date.now() / 1000);

        userStore.set(username + "/" + key, key, passwordHash, phone, points, purchases, rank, token);
        return true;        
    } catch (err) {
        console.log(err);
        return false;
    }
};

export const verification = async(verifCode) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/verification/',
            {
                code: verifCode
            }
        );

        data = JSON.parse(res);
        return data.success;
    } catch (err) {
        console.log(err);
        return false;
    }
};

export const updateAccount = async(username, phoneNumber) => {
    try {
        if (phoneNumber != userStore.phoneNumber) {
            if (verification) {
                const res = await axios.post(
                    PUBLIC_BACKEND_API + 'user/account/',
                    {
                        username: username,
                        phoneNumber: phoneNumber
                    }
                );

                data = JSON.parse(res);
                return data.success;
            }
            return false;
        } else {
            const res = await axios.post(
                PUBLIC_BACKEND_API + 'user/account/',
                {
                    username: username
                }
            );

            data = JSON.parse(res);
            return data.success;
        }
    } catch (err) {
        console.log(err);
        return false;
    }
};

export const loginWithToken = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/token-login/',
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