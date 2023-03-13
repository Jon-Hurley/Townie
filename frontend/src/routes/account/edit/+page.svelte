<script>
	import { goto } from '$app/navigation';
	import { updateAccount, deleteUser } from '../../../requests/account';
	import { userStore } from '../../../stores';
	import { buttonStyle, blueStyle, grayStyle } from '../../../css';
	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-2 bg-gray-100 h-[2px]';
	let hidingState = "Show my Exact Location";

	const form = {
		username: '',
		password: '',
        phone: '',
		showLocation: true
	};
	let errorMessage = false;

	const _deleteUser = async () => {
		errorMessage = await deleteUser();
        if (errorMessage == 10) {
            goto('/login')
            return;
        }
		if (errorMessage) {
            console.log("inside error")
			return;
		}
        console.log("past error")
		goto('/login');
	};

	const _updateUser = async () => {
		if (!form?.username?.length) {
			form.username = $userStore.username;
		}
		if (!form?.phone?.length) {
			form.phone = $userStore.phone;
		}

		errorMessage = await updateAccount(form.password, form.username, form.phone);
		if (errorMessage) {
			return;
		}

		goto('/account/');
	};
</script>

<div class="my-5 w-full">
	<div class="text-gray-700 font-bold text-3xl text-center">
		{$userStore.username}
	</div>
	<div class="text-gray-700 text-md text-center">
		#{$userStore.key}
	</div>
</div>

<div class="my-5 w-full">
	<div class="font-semibold text-lg text-center mb-3">
	</div>
	<div
            class="flex justify-center gap-2"
            style="max-height: 100%"
    >
	<button
        class="{buttonStyle} {form['showLocation'] ? blueStyle : (blueStyle)}"
        on:click={() => {
        	form['showLocation'] = !form['showLocation'];
			if (form['showLocation']) {
				hidingState = "Hide my Exact Location";
			} else {
				hidingState = "Show my Exact Location";
			}
        }}
    >
    	{hidingState}
    </button>
	</div>
</div>

<div class="max-[200px]: grid grid-cols-8 gap-0 flex items-end">
	<div class="col-span-2">
		<div class={title}>
			<div class="text-align-top">Username</div>
		</div>
	</div>

	<div class="col-start-5 col-span-4">
		<!-- Delete User Function -->
		<button
			on:click={_deleteUser}
			name="deleteAccount"
			class="group relative w-full text-center items-end rounded-md border border-transparent py-2 px-4 text-md font-medium text-indigo-600 hover:text-indigo-800 focus:outline-none"
		>
			<span class="absolute bottom-2 right-2 flex pl-4">
				<!-- Heroicon name: trash can -->
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-5 h-5"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
					/>
				</svg>
			</span>
			Delete Account
		</button>
	</div>
</div>

<hr class={hr} />
<div class="px-2 py-4">
	{$userStore.username}
	<input
		bind:value={form.username}
		type="text"
		class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
		placeholder="New Username"
	/>
</div>

<div class={title}>Phone Number</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	{$userStore.phone}
	<input
		bind:value={form.phone}
		type="text"
		class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
		placeholder="New Phone Number"
	/>
</div>

<div class={title}>Confirm Password</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	<input
		bind:value={form.password}
		type="text"
		class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
		placeholder="Enter Password to Proceed"
	/>
</div>

<div class="mt-8 mr-2 ml-2 grid grid-cols-2 gap-4 flex items-end">
	<div>
		<button
			on:click={_updateUser}
			name="save"
			class="group relative w-full text-center items-end rounded-md border border-indigo-400 py-2 px-4 text-md font-medium text-indigo-600 hover:text-indigo-800 focus:outline-none"
		>
			Save Changes
		</button>
	</div>
	<div>
		<a href="/account">
			<button
				name="cancel"
				class="group relative w-full text-center items-end rounded-md border border-red-600 py-2 px-4 text-md font-medium text-red-600 hover:text-red-800 focus:outline-red"
			>
				Cancel
			</button>
		</a>
	</div>
</div>


<!--error popup-->
{#if errorMessage}
	<div
		class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
		id="error-popup"
	>
		<div
			class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700"
		>
			<div class="mt-3 text-center">
				<div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-red-100">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-14 h-14 text-red-600"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
						/>
					</svg>
				</div>
				<h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">Error</h3>
				<div class="px-7">
					<p class="text-sm text-gray-500">
						{errorMessage}
					</p>
				</div>

				<div class="mr-2 ml-2 flex items-center px-4 py-3">
					<button
						id="ok-btn"
						on:click={() => errorMessage = null}
						class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-red-400"
					>
						OK
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
