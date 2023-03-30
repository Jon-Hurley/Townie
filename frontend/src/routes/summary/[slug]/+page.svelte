<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getSummary } from '../../../requests/search';
	import { rating } from '../../../requests/search';
	import { userStore } from '../../../stores';
	import Loading from '../../../components/loading.svelte';
	import Summary from './summary.svelte';

	let summary;
	let ratings;
	let userInGame = false;

	onMount(async () => {
		const gameKey = $page.params.slug;
		console.log($page);
		console.log({ gameKey });
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
		if (ratings == undefined) {
			ratings = {
				rating: 0,
				numRatings: 0
			};
		}

		let players = summary.players;
		let user = $userStore.username;

		console.log(user);
		for (let i = 0; i < players.length; i++) {
			if (players[i].username == user) {
				userInGame = true;
			}
		}
		console.log(userInGame);
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
