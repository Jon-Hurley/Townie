<script>
	import { goto } from '$app/navigation';
	import { signup } from '../../../requests/account';
    import Modal from '../../../components/modal.svelte';


    export let form;

    let messageObject;
    let successPopup = false;

	let otp;

    const verify = async () => {
        const res = await verifySignup(form.username, form.password, form.phone, otp);
        if (res) {
            messageObject = {status: 'success', message: "Your account as been successfully created.", dest: '/game/lobby'};
        } else {
            messageObject = {status: 'error', message: res};
        }
        console.log(res);
	};


    const resendVerification = async () => {
            const res = await signup(form.phone);
            if (!res) {
                messageObject = {status: 'error', message: "We were unable to resend your verification code at this time. Please try again."};
            }
    }
</script>



<div class="flex min-h-full full rounded-md center items-center justify-center mx-auto my-auto py-12 px-4 sm:px-6 lg:px-8">
	<div class="w-full max-w-md">
        <!-- <img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company"> -->
        <h1 class="mb-6 text-center text-2xl font-bold tracking-tight text-gray-900">
            Townie Account Creation
        </h1>
        <h3 class="text-center text-lg font-Courier New tracking-tight text-gray-700">
            Verify it's you
        </h3>
        <h5 class="mt-1 text-center font-Courier New tracking-tight text-gray-400">
            Please check your text messages for your verification code.
        </h5>

        <form class="mt-2 space-y-4" method="post">
			<input type="hidden" name="remember" value="true" />
			<div class="-space-y-px rounded-md shadow-sm">
				<div>
					<label for="verification" class="sr-only">
                        Verification
                    </label>
					<input
						bind:value={otp}
                        type="verification"
						required
						class="relative block justify-center w-full justify-center appearance-none rounded-b-md rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none sm:text-sm"
						placeholder="Verification Code"
					/>
				</div>
            </div>
            <div class="grid grid-cols-2 gap-4 flex items-end">
                <div>
                    <button
                        on:click={verify}
                        name="verify"
                        class="group relative w-full text-center items-end rounded-md border border-indigo-400 py-2 px-4 text-md font-medium text-indigo-600 hover:text-indigo-800 focus:outline-none"
                    >
                        Verify
                    </button>
                </div>
                <div>
                    <button
                        name="cancel"
                        on:click={() => {goto('/login')}}
                        class="group relative w-full text-center items-end rounded-md border border-red-600 py-2 px-4 text-md font-medium text-red-600 hover:text-red-800 focus:outline-red"
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </form>
        <div class="text-sm text-center">
            <button
            on:click={resendVerification} 
            class="font-medium text-indigo-600 mt-2 hover:text-indigo-400">
                Resend verification code.
            </button>
        </div>
    </div>
</div>

<!--Success popup-->
{#if successPopup}
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="success-popup">
        <div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
            <div class="mt-3 text-center">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-green-600">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>                     
                </div>
                <h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">Success!</h3>
                <div class="px-7">
                    <p class="text-sm text-gray-500">
                        Your account has been successfully created.
                    </p>
                </div>
        
                <div class="mr-2 ml-2 flex items-center px-4 py-3">
                    <button 
                        id="continue-btn" 
                        on:click={() => {goto('/game/lobby');}}
                        class="px-4 py-2 border border-green-600 text-green-600 text-base font-medium rounded-md w-full shadow-sm bg-green-100 hover:border-green-800 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400">
                        Continue to Townie
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}

<Modal {...messageObject} />