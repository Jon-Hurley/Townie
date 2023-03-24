import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { userStore } from './../stores'

export const login = async(username, password, remember) => {
    try {
        console.log(username, password, remember);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/login/',
            {
                password,
                username
            }
        );
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('password', password);
        if (remember) {
			localStorage.setItem('username', username);
			localStorage.setItem('password', password);
		}
        userStore.set(res.data);
        return null;
    } catch (err) {
        console.log(err)
        return err?.response?.data?.errorMessage
            || 'Connection Refused. Failed to login user. Please try again.';
    }
};

export const autoLogin = async() => {
    const sessionRes = await sessionLogin();
    if (sessionRes) {
        return true;
    }
    const localRes = await localLogin();
    return localRes;
};

export const sessionLogin = async() => {
    const username = sessionStorage.getItem('username');
    const password = sessionStorage.getItem('password');
    if (!username || !password) {
        return false;
    }
    const errorMessage = await login(username, password);
    if (errorMessage) {
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('password');
        return false;
    }
    return true;
}

export const localLogin = async() => {
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
}

export const logout = () => {
    console.log("logging out")
    userStore.set(null);
};

export const signup = async(phone) => {
    try {
        console.log(phone);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/signup/',
            {
                phone
            }
        );
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Connection Refused. User registration failed. Please try again.';
    }
};

export const verifySignup = async(username, password, phone, otp) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/verify-signup/',
            {
                phone,
                username,
                password,
                otp
            }
        );
        userStore.set(res.data);
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Incorrect OTP. Please try again.';
    }
}

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
        userStore.set(res.data)
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Connection Refused. Failed to update user. Please try again.';
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
            || 'Connection Refused. Failed to find user. Please try again.';
    }
};

export const completePasswordReset = async(phone, otp, newPassword) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/complete-password-reset/',
            {
                "phone" : phone,
                "otp" : otp,
                "newPassword" : newPassword
            }
        );
        console.log(res);
        return null;       
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Connection Refused. Failed to update password. Please try again.';
    }
};

export const deleteUser = async() => {
    try {
        const body = {
            key: get(userStore).key,
            passwordHash: get(userStore).passwordHash
        };
        console.log({body})
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/delete/',
            body
        );
        userStore.set(null);
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage
            || 'Connection Refused. Failed to delete user. Please try again.';
    }
}