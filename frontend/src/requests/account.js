import axios from 'axios';
import { PUBLIC_BACKEND_API } from '$env/static/public';
import { get } from 'svelte/store';
import { pushPopup, updateAccessToken, userStore } from './../stores';
import { goto } from '$app/navigation';
import { Game } from '../classes/Game';

export const login = async(username, password, remember, silent) => {
    try {
        console.log(username, password, remember);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/login/',
            {
                password,
                username
            }
        );

        userStore.subscribe((user) => {
            if (user?.token) {
                sessionStorage.setItem('token', user.token);
            }
        });
        if (remember) {
			localStorage.setItem('username', username);
			localStorage.setItem('password', password);
		}

        if (res.data.verifyToken) {
            return res.data;
        }

        userStore.set(res.data);
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to update user. Please try again.';
        if (!silent) pushPopup(0, err_message);
        return false;
    }
};

export const verifyLogin = async(verifyToken, otp) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/verify-login/',
            {
                verifyToken,
                otp
            }
        );
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
    const token = sessionStorage.getItem('token');
    if (!token) {
        return false;
    }

    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/token-login/',
            {
                token
            }
        );
        userStore.set(res.data);
        sessionStorage.setItem('token', res.data.token);
        return true;
    } catch (err) {
        sessionStorage.removeItem('token');
        return false;
    }
}

export const localLogin = async() => {
    const username = localStorage.getItem('username');
    const password = localStorage.getItem('password');
    if (!username || !password) {
        return false;
    }
    const errorMessage = await login(username, password, false, slient=true);
    if (errorMessage) {
        localStorage.removeItem('username');
        localStorage.removeItem('password');
        return false;
    }
    return true;
}

export const logout = () => {
    Game.leave();
    console.log("logging out")
    sessionStorage.removeItem('token');
    userStore.set(null);
};

export const signup = async (phone, username) => {
    try {
        console.log(phone, username);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/signup/',
            {
                phone,
                username
            }
        );
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to update user. Please try again.';
        pushPopup(0, err_message);
        return false;
    }
};

export const verifySignup = async (username, password, phone, otp) => {
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
        pushPopup(1, 'You have successfully created your account!');
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to update user. Please try again.';
        pushPopup(0, err_message);
        return false;
    }
}

export const updateAccount = async (password, newUsername, newPhone, newLogin2FA, newHidingState) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/update/',
            {
                token: get(userStore).token,
                password,
                newUsername,
                newPhone,
                newLogin2FA,
                newHidingState
            }
        );
        userStore.set(res.data);
        pushPopup(
            1, "Account Updated Successfully!",
            () => goto('/account')
        );
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to update user. Please try again.'
        pushPopup(0, err_message);
        return false;
    }
};

export const updatePlayableGame = async(weeklyGamePlayed, newTime) => {
    try {
        const user = get(userStore);
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/updateTime', 
            {
                key: user.key,
                username: user.username,
                passwordHash: user.passwordHash,

                weeklyGamePlayed,
                newTime
            }
        );
        userStore.set(res.data)
        return null;
    } catch (err) {
        return err?.response?.data?.errorMessage 
            || 'Connection Refused. Failed to update user. Please try again.';
    }
}

export const initiatePasswordReset = async(phone) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/initiate-password-reset/',
            {
                phone
            }
        );
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to update user. Please try again.'
        pushPopup(0, err_message);
        return false;
    }
};

export const completePasswordReset = async (phone, otp, newPassword) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/complete-password-reset/',
            {
                "phone": phone,
                "otp": otp,
                "newPassword": newPassword
            }
        );
        userStore.set(res.data);
        pushPopup(
            1, "Password Reset Successfully!",
            () => goto('/login')
        );
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to update user. Please try again.'
        pushPopup(0, err_message);
        return false;
    }
};

export const deleteUser = async() => {
    try {
        const body = {
            key: get(userStore).key,
            token: get(userStore).token
        };
        console.log({ body })
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/delete/',
            body
        );
        userStore.set(null);
        pushPopup(
            1, 'Account Deleted Successfully!',
            () => logout()
        );
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to delete user. Please try again.';
        pushPopup(0, err_message);
        return false;
    }
}