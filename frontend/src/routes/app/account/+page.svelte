<script>
	import { buttonStyle, greenStyle, redStyle, blueStyle } from '../../../css';
	import { deleteUser } from '../../../requests/account';
	import { userStore } from '../../../stores';
	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-2 bg-gray-100 h-[2px]';

	let popupOpen = false;

	const _deleteUser = async () => {
		popupOpen = false;
		const success = await deleteUser();
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

<div class="flex justify-center gap-4">
	<!-- Edit account button -->
	<a href="/app/account/edit">
		<button name="edit" class="{buttonStyle} {greenStyle} flex align-center">
			<!-- Heroicon name: pencil -->
			<div class="mr-2">Edit Account</div>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="w-6 h-6"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10"
				/>
			</svg>
		</button>
	</a>

	<!-- Delete User Function -->
	<button
		on:click={() => {
			popupOpen = true;
		}}
		name="deleteUserBtn"
		id="deleteUser-btn"
		class="{buttonStyle} {redStyle} flex"
	>
		<div class="mr-2">Delete Account</div>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="1.5"
			stroke="currentColor"
			class="w-6 h-6"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
			/>
		</svg>
	</button>
</div>

<div class="max-[200px]: grid grid-cols-8 gap-0 flex items-end">
	<div class="col-span-2">
		<div class={title}>Username</div>
	</div>
</div>

<hr class={hr} />
<div class="px-2 py-4">
	{$userStore?.username}
</div>

<div class={title}>Phone Number</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	{$userStore?.phone}
</div>

<div class={title}>Rank</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	{$userStore?.rank}
</div>

<div>
	<a href='/app/game-log'>
		<button class="{buttonStyle} {blueStyle}">
			Go to Game Logs  
		</button>
	</a>
</div>

{#if popupOpen}
	<!--deleteUser popup-->
	<div
		class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
		id="deleteUser-popup"
	>
		<div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-md bg-white">
			<div class="mt-3 text-center">
				<div class="mx-auto flex items-center justify-center rounded-full">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-12 h-12 text-red-600"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<h3 class="text-lg leading-6 font-medium text-gray-900">Are you sure?</h3>
				<div class="px-7 py-3">
					<p class="text-sm text-gray-500">
						Do you want to delete your account? This action cannot be undone.
					</p>
				</div>

				<div class="mr-2 ml-2 grid grid-cols-2 gap-4 flex items-center px-4 py-3">
					<div>
						<button
							id="cancel-btn"
							on:click={() => {
								popupOpen = false;
							}}
							class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm hover:border-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
						>
							CANCEL
						</button>
					</div>
					<div>
						<button
							id="delete-btn"
							on:click={_deleteUser}
							class="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
						>
							DELETE
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}