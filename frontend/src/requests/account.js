import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { userStore } from './../stores'

export const login = async(username, password) => {
    try {
        console.log(username, password);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/login/',
            {
                password: password,
                username: username
            }
        );
        userStore.set(res.data);
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Invalid error message.';
    }
};

export const autoLogin = async() => {
    const username = localStorage.getItem('username');
    const password = localStorage.getItem('password');
    if (!username || !password) {
        return false;
    }
    const errorMessage = await login(username, password);
    if (errorMessage) {
        localStorage.removeItem('username');
        localStorage.removeItem('password');
        return false;
    }
    return true;
};

export const logout = () => {
    console.log("logging out")
    userStore.set(null);
};

export const signup = async(username, password, phone) => {
    try {
        console.log(username, password, phone);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/signup/',
            {
                username,
                password,
                phone
            }
        );
        userStore.set(res.data);
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Invalid error message.';
    }
};

export const updateAccount = async(password, newUsername, newPhone) => {
    try {
        const user = get(userStore);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/update/',
            {
                key: user.key,
                username: user.username,
                passwordHash: user.passwordHash,

                password,
                newUsername,
                newPhone
            }
        );
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Invalid error message.';
    }
};

export const initiatePasswordReset = async(phone) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/initiate-password-reset/',
            {
                phone
            }
        );
        return null; 
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Invalid error message.';
    }
};

export const completePasswordReset = async(phone, otp, newPassword) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/complete-password-reset/',
            {
                phone,
                otp,
                newPassword
            }
        );
        console.log(res);
        return null;       
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Invalid error message.';
    }
};

export const deleteUser = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/delete/',
            {
                key: get(userStore).key,
                passwordHash: get(userStore).passwordHash
            }
        );
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Invalid error message.';
    }
}