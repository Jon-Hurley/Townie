<script>
	import { blueStyle, buttonStyle, redStyle } from '../../../../css';
	import { updateAccount } from '../../../../requests/account';
	import { userStore } from '../../../../stores';
	const title = 'text-gray-700 font-semibold text-lg mt-4';
	const hr = 'my-2 bg-gray-100 h-[2px]';

	const form = {
		password: '',
		newUsername: $userStore?.username,
		newPhone: $userStore?.phone,
		newLogin2FA: $userStore?.login2FA,
		newHidingState: $userStore?.hidingState
	};

	const _updateUser = async() => {
		if (!form?.newUsername?.length) {
			form.newUsername = $userStore.newUsername;
		}
		if (!form?.newPhone?.length) {
			form.newPhone = $userStore.newPhone;
		}
		await updateAccount(
			form.password, form.newUsername,
			form.newPhone, form.newLogin2FA, form.newHidingState
		);
	};
</script>

<div class="my-5 w-full">
	<div class="text-gray-700 font-bold text-3xl text-center">
		{$userStore?.username}
	</div>
	<div class="text-gray-700 text-md text-center">
		#{$userStore?.key}
	</div>
</div>

<div class="{title} mt-12">Username</div>
<hr class={hr} />
<div class="px-2">
	<input
		bind:value={form.newUsername}
		type="newUsername"
		id="newUsername"
		class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
		placeholder="New Username"
	/>
</div>

<div class={title}>Phone Number</div>
<hr class={hr} />
<div class="px-2 uppercase">
	<input
		bind:value={form.newPhone}
		type="newPhone"
		id="newPhone"
		class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
		placeholder="New Phone Number"
	/>
</div>

<div class={title}>Security</div>
<hr class={hr} />
<div class="px-2 flex justify-between">
	Require 2FA on Login
	<input
		type="checkbox"
		bind:checked={form.newLogin2FA}
	/>
</div>
<div class="px-2 mt-1 flex justify-between">
	Hide My Location in Game
	<input
		type="checkbox"
		bind:checked={form.newHidingState}
	/>
</div>

<div class={title}>Confirm Password</div>
<hr class={hr} />
<div class="px-2 uppercase">
	<input
		bind:value={form.password}
		type="password"
		class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
		placeholder="Enter Password to Proceed"
	/>
</div>

<div
	class="
		gap-2 flex justify-center justify-between absolute
		bottom-20
	"
	style="width: calc(100% - 2rem)"
>
	<button
		on:click={_updateUser}
		name="save"
		class="{buttonStyle} {blueStyle} w-6/12"
	>
		Save Changes
	</button>
	<a href="/app/account" class="w-6/12">
		<button
			name="cancel"
			class="{buttonStyle} {redStyle} w-full"
		>
			Cancel Changes
		</button>
	</a>
</div>