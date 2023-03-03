<script>
	import { login } from "../../requests/account";
	import { goto } from '$app/navigation';

	const form = {
		username: '',
		password: ''
	};
	let remember;

	let errorMessage = null;

    const _login = async () => {
		if (!form?.username?.length || !form?.password?.length) {
			errorMessage = 'Missing inputs. Please try again.';
			return;
		}

        errorMessage = await login(form.username, form.password);
		if (errorMessage) {
			return;
		}

		if (remember) {
			localStorage.setItem('username', form.username);
			localStorage.setItem('password', form.password);
		}
		goto('/game/join');
	};
</script>

<div class="flex h-full w-full items-center justify-center p-4">
	<div class="w-full max-w-md space-y-8">
        <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
            Log in to Account
        </h2>

		<form class="mt-8 space-y-6" >
			<input type="hidden" name="remember" value="true" />
			<div class="-space-y-px rounded-md shadow-sm">
				<div>
					<label for="username" class="sr-only">
                        Username
                    </label>
					<input
						bind:value={form.username}
						required
						class="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
						placeholder="Username"
					/>
				</div>
				<div>
					<label for="password" class="sr-only">
                        Password
                    </label>
					<input
						bind:value={form.password}
						type="password"
						autocomplete="current-password"
						required
						class="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
						placeholder="Password"
					/>
				</div>
			</div>

			<div class="flex items-center justify-between">
				<div class="flex items-center">
					<input
                        bind:checked={remember}
						type="checkbox"
						class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
					/>
					<label for="remember-me" class="ml-2 block text-sm text-gray-900">
                        Remember me
                    </label>
				</div>

				<div class="text-sm">
					<a href="/account/password-reset" class="font-medium text-indigo-600 hover:text-indigo-400">
						Forgot your password?
					</a>
				</div>
			</div>

            <button
                on:click={_login}
                class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
                <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                    <!-- Heroicon name: mini/lock-closed -->
                    <svg
                        class="h-5 w-5 text-indigo-400 group-hover:text-indigo-300"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        aria-hidden="true"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </span>
                Log in
            </button>

			
			<div class="text-md text-center">
				<a href="/signup" class="font-medium text-indigo-600 hover:text-indigo-400">
					New around here?
				</a>
			</div>
		</form>
	</div>
</div>

<!--failed login popup-->
{#if errorMessage}	
	<div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="loginFailed-popup">
		<div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
			<div class="mt-3 text-center">
				<div class="mx-auto flex items-center justify-center rounded-full">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-red-600">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
						</svg>						  
				</div>
				<h3 class="text-lg leading-6 font-medium text-gray-900">Login Failed</h3>
				<div class="px-7">
					<p class="text-sm text-gray-500">
						{errorMessage}
					</p>
				</div>
	
				<div class="mr-2 ml-2 flex items-center px-4 py-3">
					<button 
						id="ok-btn" 
						on:click={() => errorMessage = false}
						class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
					>
						OK
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}