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
        console.log(res);
        let data = res.data;
        console.log(res.data)
        let success = data.success;
        if (success == false) {
            return false;
        }
        let key = data.key;
        let phone = data.phoneNumber;
        let points = data.points;
        let purchases = data.purchases;
        let rank = data.rank;
        console.log(res.data);
        userStore.set(res.data);

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

        let data = res.data;
        console.log(res.data)
        let success = data.success;
        if (success == false) {
            return false;
        }
        let key = data.key;
        let phone = data.phoneNumber;
        let points = data.points;
        let purchases = data.purchases;
        let rank = data.rank;
        console.log(res.data);
        userStore.set(res.data);
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