<script>
	import { goto } from '$app/navigation';
	import Modal from '../../components/modal.svelte';
    import { signup, verifySignup } from "../../requests/account";

	let username = '';
	let password = '';
    let phone = '';
    let confirmPassword = '';
    let otp = '';

    let messageObj = {
        status: 0,
        message: null,
        dest: null
    };

    let page = 0;
    let confirmationPopup = false;

    const confirm = async () => {
        if (!password?.length || !username?.length || !phone?.length) {
            messageObj = {
                status: 0,
                message: 'Missing inputs. Please try again.'
            };
            return;
        }

        if (password !== confirmPassword) {
            messageObj = {
                status: 0,
                message: 'Your password inputs do not match.'
            }
            return;
        }

        const formattedPhone = '+1' + phone.replace(/\D/g, '');
        if (formattedPhone.toString().length !== 12) {
            messageObj = {
                status: 0,
                message: 'Invalid phone input.'
            }
            return;
        }

        confirmationPopup = true;
	};

    const _signup = async() => {
        confirmationPopup = false;
        
        const formattedPhone = '+1' + phone.replace(/\D/g, '');
        const errorMessage = await signup(formattedPhone);
        if (errorMessage) {
            messageObj = {
                status: 0,
                message: errorMessage
            };
            return;
        }
        page = 1;
    }

    const verify = async() => {
        const formattedPhone = '+1' + phone.replace(/\D/g, '');
        const errorMessage = await verifySignup(username, password, formattedPhone, otp);
        if (errorMessage) {
            messageObj = {
                status: 0,
                message: errorMessage
            };
            return;
        }

        messageObj = {
            status: 1,
            message: "You have successfully created your account!",
            dest: '/game/join'
        };
        goto('/account')
    }
</script>

<Modal
    {...messageObj}
/>

{#if page === 0}
    <div class="flex h-full w-full mx-auto items-center justify-center px-4 sm:px-6 lg:px-8">
        <div class="w-full max-w-md space-y-8">
            <!-- <img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company"> -->
            <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                Create Account
            </h2>

            <form class="mt-8 space-y-6">
                <input type="hidden" name="remember" value="true" />
                <div class="-space-y-px rounded-md shadow-sm">
                    <div>
                        <label for="username" class="sr-only">
                            Username
                        </label>
                        <input
                            bind:value={username}
                            type="username"
                            class="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                            placeholder="Username"
                        />
                    </div>
                    <div>
                        <label for="password" class="sr-only">
                            Password
                        </label>
                        <input
                            bind:value={password}
                            type="password"
                            class="relative block w-full appearance-none rounded-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                            placeholder="Password"
                        />
                    </div>
                    <div>
                        <label for="password" class="sr-only">
                            Confirm Password
                        </label>
                        <input
                            bind:value={confirmPassword}
                            type="password"
                            class="relative block w-full appearance-none rounded-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                            placeholder="Confirm Password"
                        />
                    </div>
                    <div>
                        <label for="phone-number" class="sr-only">
                            Phone Number
                        </label>
                        <input
                            bind:value={phone}
                            class="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                            placeholder="Phone Number"
                        />
                    </div>
                </div>

                    <button
                        on:click={confirm}
                        class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    >
                        Sign Up
                    </button>

                    <div class="text-md text-center">
                        <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-400">
                            Back to login
                        </a>
                    </div>
            </form>
        </div>
    </div>
{:else}
    <div class="flex h-full w-full mx-auto items-center justify-center px-4 sm:px-6 lg:px-8">
        <div class="w-full max-w-md space-y-8">
            <!-- <img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company"> -->
            <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                Verify Phone Number
            </h2>

            <form class="mt-8 space-y-6">
                <input type="hidden" name="remember" value="true" />
                <div class="-space-y-px rounded-md shadow-sm">
                    <div>
                        <label for="username" class="sr-only">
                            OTP
                        </label>
                        <input
                            bind:value={otp}
                            class="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                            placeholder="Enter the OTP sent to your phone."
                        />
                    </div>
                </div>

                <button
                    on:click={verify}
                    class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                    Verify
                </button>
                <button
                    on:click={_signup}
                    class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                    Resend OTP.
                </button>

                <div class="text-md text-center">
                    <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-400">
                        Quit to login
                    </a>
                </div>
            </form>
        </div>
    </div>
{/if}

<!--confirmation popup-->
{#if confirmationPopup}
    <div class="z-50 fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="success-popup">
        <div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
            <div class="mt-3 text-center">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-indigo-600">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                    </svg>
                </div>

                <h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">Please Confirm Inputs</h3>
                <div class="my-2 px-4 text-left space-y-2">
                    <p class="text-sm text-gray-500">
                        Username: {username}
                    </p>
                    <p class="text-sm text-gray-500">
                        Phone Number: {phone}
                    </p>
                </div>
        
                <div class="mr-2 ml-2 grid grid-cols-2 gap-4 flex items-center px-4 py-3">
                    <div>
                        <button 
                            id="cancel-btn" 
                            on:click={() => confirmationPopup = false}
                            class="px-4 py-2 border border-indigo-600 text-indigo-600 text-base font-medium rounded-md w-full shadow-sm hover:border-indigo-800 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                        >
                            CANCEL
                        </button>
                    </div>
                    <div>
                        <button 
                            id="confirm-btn" 
                            on:click={_signup}
                            class="px-4 py-2 bg-indigo-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-indigo-800 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                        >
                            CONFIRM
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}