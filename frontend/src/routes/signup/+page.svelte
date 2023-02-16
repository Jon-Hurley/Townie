<script>
	import { goto } from '$app/navigation';
	import { PUBLIC_BACKEND_API } from '$env/static/public';
    import axios from 'axios';

    let remember;
	const form = {
		username: '',
		password: '',
        phoneNumber: ''
	};

    const signup = async () => {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/signup/'
        );
        goto('/verification');
        console.log(res);
	};
</script>

<div class="flex min-h-full items-center justify-center mt-20 py-12 px-4 sm:px-6 lg:px-8">
	<div class="w-full max-w-md space-y-8">
        <!-- <img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company"> -->
        <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
            Create Account
        </h2>

		<form class="mt-8 space-y-6" method="post">
			<input type="hidden" name="remember" value="true" />
			<div class="-space-y-px rounded-md shadow-sm">
				<div>
					<label for="username" class="sr-only">
                        Username
                    </label>
					<input
						bind:value={form.username}
                        type="username"
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
						required
						class="relative block w-full appearance-none rounded-none rounded-none border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
						placeholder="Password"
					/>
				</div>
                <div>
					<label for="phone-number" class="sr-only">
                        Phone Number
                    </label>
					<input
						bind:value={form.phoneNumber}
						type="phoneNumber"
						required
						class="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
						placeholder="Phone Number"
					/>
				</div>
			</div>

                <button
                    on:click={signup}
                    type="submit"
                    class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                        <!-- Heroicon name: mini/lock-closed -->
                        <svg
                            class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400"
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
                    Sign Up
                </button>

                <div class="text-sm text-center">
                    <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
                        Back to login
                    </a>
                </div>
		</form>
	</div>
</div>