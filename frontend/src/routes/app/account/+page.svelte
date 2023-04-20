<script>
	import { onMount } from 'svelte';
	import { buttonStyle, greenStyle, blueStyle, hr, largeTitle } from '../../../css';
	
	import Username from '../../../general-components/username.svelte';
	import Delete from './delete.svelte';
	import Premium from '../../../general-components/premium.svelte';
	import Purchases from './purchases.svelte';

	import { pushPopup, userStore } from '../../../stores';
	import { pointsToLevel, pointsToProgress, pointsToRank } from './../../../util'

	const title = 'font-semibold text-lg mt-6';

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

<div class="{largeTitle} pb-4">
	<Username boldness={'bold'}/>
	<div class="text-sm font-normal mt-1">
		{pointsToRank($userStore?.cumPoints)}
		&bull;
		{$userStore.points} Points
	</div>
</div>

<div class="flex flex-wrap justify-center gap-2">
	<!-- Game Log Button -->
	<a href='/app/game-log'>
		<button class="{buttonStyle} {blueStyle}" title="Game Log">
			<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
				<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z" />
			</svg>
		</button>
	</a>

	<!-- Edit Account Button -->
	<a href="/app/account/edit">
		<button
			name="edit"
			class="{buttonStyle} {greenStyle} flex align-center"
			title="Edit Account"
		>
			<!-- Heroicon name: pencil -->
			<!-- <div class="mr-2">Edit Account</div> -->
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

	<!-- Delete Account Button -->
	<Delete/>

	<!-- Premium Button -->
	<Premium simplified={false}/>
</div>

<div class={title}>
	Level {pointsToLevel($userStore.cumPoints)}
</div>
<hr class={hr} />
<meter
	id="xp-meter"
	class="h-8 w-full px-2 shimmer"
	min="0"
	max="1"
	value={pointsToProgress($userStore.cumPoints)}
/>

<div class={title}>
	Purchases
</div>
<hr class={hr} />
<Purchases/>
