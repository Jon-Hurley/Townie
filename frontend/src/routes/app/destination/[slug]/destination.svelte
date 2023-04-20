<script>
	import { primaryColor, pushPopup } from '../../../../stores';
	import { buttonStyle, indigoStyle, largeTitle } from '../../../../css';
	import { submitDestRating } from '../../../../requests/account';
	
	import Share from '../../../../general-components/share.svelte';
	import DestinationRating from './destinationRating.svelte';
	
	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-1 bg-gray-100 h-[2px]';

	export let destination, theme, userRating, reload;
	
	$: tips = destination?.tips || [];
	let tipIndex = 0;
</script>

<div class="my-5 w-full">
	<div class="{largeTitle}">
		{destination.name}
	</div>
</div>

<Share header="Share Destination!"/>

<DestinationRating
	initialUserRating={userRating?.rating || 0}
	showRateable={true}
	destination={destination}
	reload={reload}
/>

<div class={title}>
	Tips
</div>
<hr class={hr} />
<div
	class="
		flex justify-center items-center
		relative border-2 rounded-xl min-h-[100px]
		mx-2 my-4 p-2 border-{$primaryColor}-500
	"
>
	<div class=''>
		{tips.length ? tips[tipIndex] : 'No tips to display'}
	</div>
		
	{#if tips.length >= 1}
		<button
			class="absolute left-[-14px] text-{$primaryColor}-500 bg-white"
			on:click={() => tipIndex = (tipIndex - 1 + tips.length) % tips.length}
		>
			<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
		</button>
		<button
			class="absolute right-[-14px] text-{$primaryColor}-500 bg-white"
			on:click={() => tipIndex = (tipIndex + 1) % tips.length}
		>
			<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
				<path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
			</svg>
		</button>
		<div class="absolute bottom-[-12px] px-1 text-{$primaryColor}-500 bg-white">
			{tipIndex + 1} of {tips.length}
		</div>
	{/if}

</div>

<hr class={hr} />
<button
	class="{buttonStyle} {indigoStyle} my-4"
	on:click={() => window.close()}
>
	Return To Game
</button>
<hr class={hr} />