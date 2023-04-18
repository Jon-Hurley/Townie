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

        if (remember) {
			localStorage.setItem('username', username);
			localStorage.setItem('password', password);
		}

        if (res.data.verifyToken) { // 2FA needed.
            return res.data;
        }
        // 2FA not needed.
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
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to login user. Please try again.';
        pushPopup(0, err_message);
        return false;
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
    const success = await login(username, password, false, true);
    if (!success) {
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
                            || 'Connection Refused. Failed to signup user. Please try again.';
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
        pushPopup(
            1, 'You have successfully created your account!',
            () => goto('/app/tutorial')
        );
        return true;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to update user. Please try again.';
        pushPopup(0, err_message);
        return false;
    }
}

export const updateAccount = async (password, newUsername, newPhone, newLogin2FA, newHidingState, newShowTimes) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/update/',
            {
                token: get(userStore).token,
                password,
                newUsername,
                newPhone,
                newLogin2FA,
                newHidingState,
                newShowTimes
            }
        );
        userStore.set(res.data);
        pushPopup(
            1, "Account Updated Successfully!",
            () => goto('/app/account')
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
            PUBLIC_BACKEND_API + 'user/updateTime/', 
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

export const initiatePremiumSession = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/initiate-subscription/',
            {
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
        const url = res.data.url;
        if (url) {
            window.open(url, '_blank').focus();
        }
    } catch (err) {
        console.log(err)
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to process payments at this time. Please try again later.";
        pushPopup(0, err_message);
    }
}

export const cancelPremium = async() => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/cancel-subscription/',
            {
                token: get(userStore).token
            }
        );
        updateAccessToken(res);
    } catch (err) {
        console.log(err)
        const err_message = err?.response?.data?.errorMessage
                            || "Unable to process cancelation at this time. Please contact customer support at (123)456-7890.";
        pushPopup(0, err_message);
    }
}

export const spendPoints = async(option) => {
    try {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/spend-points/',
            {
                token: get(userStore).token,
                option: option
            }
        )
        if (!res.data) {
            pushPopup(0, 'Connection Refused. Failed to spend points. Please try again.');
            return false;
        }
        updateAccessToken(res);
        console.log(res);
        userStore.set(res.data);
        return res;
    } catch (err) {
        const err_message = err?.response?.data?.errorMessage
                            || 'Connection Refused. Failed to spend points. Please try again.';
        pushPopup(0, err_message);
        return false;
    }
}