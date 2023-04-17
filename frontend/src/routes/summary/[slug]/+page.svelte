<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getSummary } from '../../../requests/search';
	import { rating } from '../../../requests/search';
	import { userStore } from '../../../stores';
	import Loading from '../../../general-components/loading.svelte';
	import Summary from './summary.svelte';

	let userInGame;
	let summary;
	let ratings;

	onMount(async () => {
		let gameKey = $page.params.slug;
		if (!gameKey) {
			const url = window.location.href;
			gameKey = url.substring(url.lastIndexOf('/') + 1);
		}

		summary = await getSummary(gameKey);
		summary.numFinished = summary.players.filter(
			(player) => player.destinationIndex === summary.destinations.length - 1
		).length;
		console.log(summary);

		let theme = 'error';
		if (summary) {
			theme = summary.game.settings.theme;
		}
		console.log(summary);
		ratings = await rating(summary.game.settings.theme);
		if (!ratings) {
			ratings = {
				rating: 0,
				numRatings: 0
			};
		}

		let players = summary.players;
		let username = $userStore?.username;
		userInGame = !!players.find((x) => x?.username == username);
	});
</script>

{#if summary}
	{#if ratings}
		<div class="h-full flex flex-col">
			<Summary {summary} {ratings} {userInGame} />
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
