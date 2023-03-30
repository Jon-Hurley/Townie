<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getSummary } from '../../../requests/search';
	import { rating } from '../../../requests/search';
	import { userStore } from '../../../stores';
	import Loading from '../../../general-components/loading.svelte';
	import Summary from './summary.svelte';

	let summary;
	let ratings;
	let userInGame = false;

	onMount(async () => {
		const gameKey = $page.params.slug;
		console.log($page);
		console.log({ gameKey });
		summary = await getSummary(gameKey);

		let theme = 'error';
		if (summary) {
			theme = summary.game.settings.theme;
		}
		console.log(theme);
		ratings = await rating(summary.game.settings.theme);
		if (ratings == undefined) {
			ratings = {
				rating: 0,
				numRatings: 0
			};
		}

		let players = summary.players;
		let user = $userStore?.username;
		if (players.includes(user)) {
			userInGame = true;
		}

		console.log(ratings);
		console.log(summary);
	});
</script>

{#if summary}
	{#if ratings}
		<div class="h-full flex flex-col">
			<Summary {summary} {ratings} />
		</div>
	{:else}
		<Loading />
	{/if}
{:else if summary === false}
	<div class="h-full flex flex-col">
		<h1 class="text-2xl mt-4 text-center text-gray-700">No game summary found.</h1>
	</div>
{:else}
	<Loading />
{/if}