<script>
	import { goto } from '$app/navigation';
	import { verification } from "../../../requests/account";

    let remember;
	const form = {
		verification: ''
	};

    const verify = async () => {
        const res = await verification(form.verification);
        if (res) {
            goto('/lobby');
        }
        console.log(res);
	};

    const resendVerification = async () => {

    }
</script>

<div class="flex min-h-full full rounded-md center items-center justify-center mt-20 py-12 px-4 sm:px-6 lg:px-8">
	<div class="w-full max-w-md">
        <!-- <img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company"> -->
        <h1 class="mb-6 text-center text-5xl font-bold tracking-tight text-gray-900">
            Townie Account Creation
        </h1>
        <h3 class="text-center text-2xl font-Courier New tracking-tight text-gray-900">
            Verify it's you
        </h3>
        <h5 class="mt-1 text-center font-Courier New tracking-tight text-gray-900">
            Please check your email for your verification code.
        </h5>

        <form class="mt-2 space-y-6" method="post">
			<input type="hidden" name="remember" value="true" />
			<div class="-space-y-px rounded-md shadow-sm">
				<div>
					<label for="verification" class="sr-only">
                        Verification
                    </label>
					<input
						bind:value={form.verification}
                        type="verification"
						required
						class="relative block justify-center w-full justify-center appearance-none rounded-b-md rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none sm:text-sm"
						placeholder="Verification Code"
					/>
				</div>
            </div>
            <button
                    on:click={verify}
                    type="submit"
                    class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-grey-100 focus:outline-gray-900 focus:ring-2 focus:ring-offset-2"
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
                    Verify
                </button>
        </form>
        <div class="text-sm text-center">
            <button
            on:click={resendVerification()} 
            class="font-medium text-indigo-600 mt-2 hover:text-indigo-400">
                Resend Email
            </button>
        </div>
    </div>
</div>