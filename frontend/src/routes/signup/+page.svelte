<script>
	import { goto } from '$app/navigation';
    import { signup } from "../../requests/account";


	let username = '';
	let password = '';
    let phone = '';

    let successPopup = false;
    let errorPopup = false;
    let phoneError = false;
    let noInputEror = false;

    const _signup = async () => {
        if (password == '' || username == '' || phone == '') {
            noInputEror = true;
        } else{
            if (phone.toString().length != 10 || isNaN(phone)) {
                phoneError = true;
            } else {
                phone = "+1" + phone;
                const res = await signup(username, password, phone);
                if (res) {
                    successPopup = true;
                } else {
                    errorPopup = true;
                }
                console.log(res);
            }
            username = '';
            password = '';
            phone = '';
        }
	};

</script>

<div class="flex min-h-full mx-auto items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
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
                    on:click={_signup}
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

{#if successPopup}
    <!--Success popup-->
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

{#if errorPopup}
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
                        Your account has not been registered. Please try again.
                    </p>
                </div>
        
                <div class="mr-2 ml-2 flex items-center px-4 py-3">
                    <button 
                        id="ok-btn" 
                        on:click={() => {errorPopup = false;}}
                        class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-red-400">
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
                        The phone number you input is not the correct length or incorrectly formatted. Numbers should not include any special characters in phone number.
                    </p>
                </div>
        
                <div class="mr-2 ml-2 flex items-center px-4 py-3">
                    <button 
                        id="ok-btn" 
                        on:click={() => {phoneError = false;}}
                        class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-red-400">
                        OK
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}

{#if noInputEror}
    <!--no input error popup-->
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
                        Missing inputs. Please try again.
                    </p>
                </div>
        
                <div class="mr-2 ml-2 flex items-center px-4 py-3">
                    <button 
                        id="ok-btn" 
                        on:click={() => {noInputEror = false;}}
                        class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-red-400">
                        OK
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}