<script>
    import { goto } from '$app/navigation';
	import { updateAccount } from "../../../requests/account";
    import { userStore } from "../../stores";

    let remember;
	const form = {
		username: '',
		phoneNumber: ''
	};

    const update = async () => {
        if (username == null) {
            username = userStore.username;
        }
        if (phoneNumber == null) {
            phoneNumber = userStore.phoneNumber;
        }
        
        const res = await updateAccount(form.username, form.password);
		if (res) {
			goto('/lobby');
		}
        console.log(res);
	};
</script>

<div class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-6">
        <h1 class="text-center text-3xl font-bold tracking-tight text-gray-900">
            Update My Account
        </h1>
        <form class="text-left space-y-2">
            <h1> New Username: </h1>
            <input type="hidden" name="remember" value="true"/>
            <div>
                <label for="New Username" class="sr-only">
                    New Username
                </label>
                <input
                    bind:value={form.username}
                    required
                    class="relative block w-full appearance-none rounded-none rounded-t-md rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                    placeholder="New Username"
                />
            </div>

            <h1> Phone Number: </h1>
            <script type="text/javascript">
                document.write(userStore.phoneNumber);
            </script>
            <input type="hidden" name="remember" value="true"/>
            <div>
                <label for="New Username" class="sr-only">
                    New Phone Number
                </label>
                <input
                    bind:value={form.phoneNumber}
                    required
                    class="relative block w-full appearance-none rounded-none rounded-t-md rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                    placeholder="New Phone Number"
                />
            </div>
            <button
                on:click={update}
                type="submit"
                class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
                Submit
            </button>
        </form>
        <a href="/initiate-password-reset" class="mt-8 font-medium text-indigo-600 hover:text-indigo-400">
            Reset Password
        </a>
    </div>
</div>

  