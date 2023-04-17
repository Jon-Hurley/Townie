<script>
	import Username from '../../../../general-components/username.svelte';
	import Share from './share.svelte';
	import Rating from './rating.svelte';

	import { primaryColor } from '../../../../stores';
	import { redStyle, greenStyle, hr, largeTitle } from '../../../../css';
	const title = 'font-semibold text-lg mt-6';

	export let summary, userInGame, reloadGameSummary;

	const getTime = (totalSeconds) => {
		const date = new Date(null);
		date.setSeconds(totalSeconds);
		return date.toISOString().slice(11, 19);
	}
</script>

<div class="{largeTitle}">
	<div class="mb-1">
		Game #{summary.game._key}
	</div>
	<div class="text-gray-700 text-sm text-center font-normal">
		<div>
			Played on {new Date(summary.game.startTime).toLocaleDateString()}
		</div>
		<div class="text-center text-green-600">
			Estimated to take {getTime(summary.game.trueCompletionTime)}s
		</div>
	</div>
</div>

<Share/>

<Rating
	{userInGame}
	{summary}
	{reloadGameSummary}
/>

<div class={title}>Destinations</div>
<hr class={hr} />
<div>
	<div class="flex flex-wrap justify-center gap-4 p-2">
		{#if !summary.destinations.length}
			<div>
				No destinations to display.
			</div>
		{/if}

		{#each summary.destinations as p}
			<div
				class="
					border-[2px] border-{$primaryColor}-500
					text-{$primaryColor}-500
					rounded-2xl w-full p-4 pl-6
					relative
					cursor-pointer
					hover:scale-105
					flex flex-col justify-center
                "
			>
				<div class="font-semibold text-full">
					{p.name}
				</div>
				<div class="text-sm">
					{p.points} points | {getTime(p.timeToCompletion)}s away
				</div>
				<div class="absolute left-[-12px] bg-white px-1">
					#{p.index + 1}
				</div>
			</div>
		{/each}
	</div>
</div>

<div class={title}>Participants</div>
<hr class={hr} />
<div>
	<div class="flex flex-wrap justify-center gap-2 p-2">
		{#if !summary.players.length}
			<div>No participants to display.</div>
		{/if}

		{#each summary.players as r}
			<div
				class="
					border-[2px] rounded-2xl w-24 h-24 p-2
					relative cursor-pointer hover:scale-105
					flex flex-col justify-center items-center
					{r.destinationIndex === summary.destinations.length
						? greenStyle
						: redStyle
					}
				"
			>
				<a href={'/app/user/' + r.key}>
					<Username user={r} boldness="semibold"/>
				</a>
				<div class="text-sm">
					{r.points} points
				</div>
			</div>
		{/each}
	</div>
</div>