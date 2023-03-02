<script>
	import { initiatePasswordReset } from "../../requests/account";
	import { goto } from '$app/navigation';
	import { userStore } from "../../stores";

    let phone;
	let notFoundPopup = false;
    let phoneError = false;

    const _submit = async () => {

        if (phone.toString().length != 10 || isNaN(phone)) {
            phoneError = true;
        } else {
            phone = "+1" + phone;
            console.log(phone);
            const res = await initiatePasswordReset(phone);
            if (res) {
                goto('/password-reset');
            } else {
                notFoundPopup = true;
            }
        }
        phone = '';
        console.log(res);
	};
</script>

<form id="phoneInput">
<div class="fixed inset-0 bg-gray-100 overflow-y-auto h-full w-full">
    <div class="relative top-60 mx-auto p-3 w-80 shadow-lg rounded-lg border bg-white">
        <div class="mt-3 text-left">
            <div class="px-7">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Enter phone number</h3>
                <p class="mt-3 text-sm text-gray-500">
                   Please enter the phone number linked to your account. Do not include any special characters.
                </p>
            </div>

            <div class="mt-2 mr-2 ml-2 flex items-center px-4 py-3">
                <label for="username" class="sr-only">
                    Phone Number
                </label>
                <input 
                    name: phone
                    placeholder="Phone number"
                    bind:value={phone}
                    class="relative block w-full appearance-none rounded-b-md rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm">
            </div>
        </div>
        <div class="mt-2 mx-6 mb-3 grid grid-cols-2 gap-4 flex items-end">
            <div>
                <button
                    on:click={_submit}
                    name=submit
                    class="group relative w-full text-center items-end rounded-md border border-gray-600 py-2 px-4 text-md font-medium text-gray-600 hover:text-gray-800 focus:outline-gray-600">
                    Submit
                </button> 
            </div>
            <div>
                <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-400">
                <button
                    name=cancel
                    class="group relative w-full text-center items-end rounded-md border border-red-600 py-2 px-4 text-md font-medium text-red-600 hover:text-red-800 focus:outline-red-600">
                    Cancel
                </button> 
                </a>
            </div>
        </div>
    </div>
</div>
</form>

{#if notFoundPopup}
    <!--error popup-->
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="error-popup">
        <div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
            <div class="mt-3 text-center">
                <div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-red-100">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-14 h-14 text-red-600">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                    </svg>                 
                </div>
                <h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">Error</h3>
                <div class="px-7">
                    <p class="text-sm text-gray-500">
                        We could not find your account in our database. Please try again.
                    </p>
                </div>
        
                <div class="mr-2 ml-2 flex items-center px-4 py-3">
                    <button 
                        id="ok-btn" 
                        on:click={() => {notFoundPopup = false;}}
                        class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 hover:bg-red-400 focus:outline-none focus:ring-2 focus:ring-red-400">
                        OK
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}

{#if phoneError}
    <!--phone error popup-->
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="error-popup">
        <div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
            <div class="mt-3 text-center">
                <div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-red-100">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-14 h-14 text-red-600">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                    </svg>                 
                </div>
                <h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">Error</h3>
                <div class="px-7">
                    <p class="text-sm text-gray-500">
                        The phone number you input is not the correct length or incorrectly formatted. Please try again.
                    </p>
                </div>
        
                <div class="mr-2 ml-2 flex items-center px-4 py-3">
                    <button 
                        id="ok-btn" 
                        on:click={() => {phoneError = false;}}
                        class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 hover:bg-red-400 focus:outline-none focus:ring-2 focus:ring-red-400">
                        OK
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}
