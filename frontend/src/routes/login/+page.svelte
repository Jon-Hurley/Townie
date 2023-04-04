<script>
	import { login, verifyLogin } from '../../requests/account';
	import { goto } from '$app/navigation';
	import { pushPopup } from '../../stores';
	import Loading from '../../general-components/loading.svelte';

	const form = {
		username: '',
		password: '',
		remember: false,
		verifyToken: undefined,
		otp: ''
	};
	let loading = false;

	const _login = async () => {
		loading = true;
		if (!form?.username?.length || !form?.password?.length) {
			pushPopup(0, 'Missing inputs. Please try again.');
			return;
		}

		const res = await login(form.username, form.password, form.remember);
		loading = false;
		if (res?.verifyToken) {
			// 2FA. Need to verify
			form.verifyToken = res.verifyToken;
			return;
		}
	};

	const verify = async () => {
		loading = true;
		const succ = await verifyLogin(form.verifyToken, form.otp);
		loading = false;
	};
</script>

{#if loading}
	<Loading/>
{:else if !form.verifyToken}
	<div class="flex h-full w-full items-center justify-center p-4">
		<div class="w-full max-w-md space-y-8">
			<h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
				Log in to Account
			</h2>

			<form class="mt-8 space-y-6">
				<input type="hidden" name="remember" value="true" />
				<div class="-space-y-px rounded-md shadow-sm">
					<div>
						<label for="username" class="sr-only"> Username </label>
						<input
							bind:value={form.username}
							required
							class="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
							placeholder="Username"
						/>
					</div>
					<div>
						<label for="password" class="sr-only"> Password </label>
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
							bind:checked={form.remember}
							type="checkbox"
							class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
						/>
						<label for="remember-me" class="ml-2 block text-sm text-gray-900"> Remember me </label>
					</div>

					<div class="text-sm">
						<a
							href="/account/password-reset"
							class="font-medium text-indigo-600 hover:text-indigo-400"
						>
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
						<label for="username" class="sr-only"> OTP </label>
						<input
							bind:value={form.otp}
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
					on:click={_login}
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