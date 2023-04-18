<script>
	import { onMount } from 'svelte';

	import { pushPopup } from '../../../stores';
	import { buttonStyle, redStyle, greenStyle, indigoStyle } from '../../../css';
	import { submitDestRating } from '../../../requests/search';
	import Rating from '../../../general-components/rating.svelte';
	
	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-1 bg-gray-100 h-[2px]';

	export let destination;
	
	let tipIndex = 0;

	const _submitDestRating = async (userRating) => {		
		pushPopup({
			status: 1,
			message: 'Your rating has been received'
		});

		const success = await submitDestRating(destination._key, userRating, newNumRatings + 1);
		if (success) {
			//reload()
		}
	};
</script>

<div class="my-5 w-full">
	<div class="text-gray-700 font-bold text-3xl text-center">
		Destination: {destination.name}
	</div>
	<!-- <div class="text-gray-700 text-md text-center">
		{new Date(summary.game.startTime).toLocaleString()}
	</div> -->
</div>

<div class={title}>Share Destination!</div>
<hr class={hr} />

<div class="flex flex-row justify-center">
	{#each media as media}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			style="display: flex; justify-content: center;"
			class="
			border-gray-400 border-2 rounded-full
			p-3 m-0
			text-indigo-500 font-semibold
			w-24 h-24
			flex flex-col items-center justify-center
			text-xs
			hover:scale-110 duration-200
			z-100
			overflow-visible
			cursor-pointer
		"
			on:click={() => {
				if (media.name === 'Copy Link') {
					navigator.clipboard.writeText('' + window.location.href);
					pushPopup(1, 'Link copied to clipboard!');
				} else {
					window.open(media.link, '_blank');
				}
			}}
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 48 48"
				stroke-width="1.5"
				stroke="currentColor"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d={media.icon} />
			</svg>

			<div class="text-center">{media.name}</div>
		</div>
	{/each}
</div>
<hr class={hr} style="margin-top:10px;" />

<div class={title} style="margin-bottom:10px;">
	Theme: <div class={indigoStyle} style="display:inline-block">
		{destination.theme}
	</div>
	<div
		id="star-rating"
		class="fa-pull-right {buttonStyle}"
		style="display:inline-block;text-align:right;"
	/>
	<hr class={hr} />
</div>

<Rating
	initialUserRating={destination?.userRating?.rating || 0}
	onSubmit={_submitDestRating}
/>

<div class={title}>Tips</div>
<hr class={hr} />
<div class="h-full">
	<div class="flex flex-wrap justify-center gap-2 px-2 py-4">
		{#if !destination.tips.length}
			<div>No tips to display.</div>
		{:else}
			<ul>
				{#each destination.tips as t, i}
					{#if i === tipIndex}
						<li class={buttonStyle} style="display:block;margin:5px">{t}</li>
					{/if}
				{/each}
				<!-- <li class={buttonStyle} style="display:block;margin:5px">Another one</li> -->
			</ul>
			<div style="display:block;">
				<button
					class="{buttonStyle}{indigoStyle}"
					style="float:left;"
					on:click={() =>
						(tipIndex =
							(tipIndex - 1 + destination.tips.length) % destination.tips.length)}
				>
					&larr;
				</button>
				<button
					class="{buttonStyle}{indigoStyle}"
					style="float:right;"
					on:click={() =>
						(tipIndex =
							(tipIndex + 1 + destination.tips.length) % destination.tips.length)}
				>
					&rarr;
				</button>
				<div class={title} style="display:block;text-align:center;">
					Tip {tipIndex + 1} of {destination.tips.length}
				</div>
			</div>
		{/if}
	</div>
</div>

<button class="{buttonStyle}{indigoStyle}" onclick="window.close()">Return To Game</button>
