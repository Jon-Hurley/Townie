<script>
	import { buttonStyle, greenStyle, blueStyle } from '../../../css';
	
	import Username from '../../../general-components/username.svelte';
	import Delete from './delete.svelte';

	import { pushPopup, userStore } from '../../../stores';
	import Premium from '../../../general-components/premium.svelte';
	import { onMount } from 'svelte';

	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-2 bg-gray-100 h-[2px]';

	onMount(() => {
		const urlParams = new URLSearchParams(window.location.search);
		if (urlParams.has('success')) {
			const wasSuccessful = urlParams.get('success') === 'true';
			if (wasSuccessful) {
				pushPopup({
					status: 1,
					message: 'You have successfully activated premium. You can now access all premium features.'
				})
			} else {
				pushPopup({
					status: 0,
					message: 'Failed to activate premium. Please contact customer support at (123)456-7890.'
				})
			}
		}
	})
</script>

<div class="my-5 w-full pb-4 text-center text-gray-700 font-bold text-3xl">
	<Username boldness={'bold'}/>
</div>

<div class="flex justify-center gap-2">
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
	<Delete/>
</div>

<div class="flex justify-center mt-2 gap-2">
	<a href='/app/game-log'>
		<button class="{buttonStyle} {blueStyle}">
			Game Logs  
		</button>
	</a>
	<Premium simplified={false}/>
</div>

<div class={title}>Phone Number</div>
<hr class={hr} />
<div class="p-2 uppercase">
	{$userStore?.phone}
</div>

<div class={title}>Rank</div>
<hr class={hr} />
<div class="p-2 uppercase">
	{$userStore?.rank}
</div>