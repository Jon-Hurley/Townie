<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	import Loading from '../../../../general-components/loading.svelte';
	import Summary from './summary.svelte';

	import { getSummary } from '../../../../requests/search';
	
	import { userStore } from '../../../../stores';
	
	let summary;
	let loading = false;
	$: userInGame = !!summary?.players?.find(x => x?.username == $userStore.username);

	const _loadGameSummary = async () => {
		loading = true;
		let gameKey = $page.params.slug;
		summary = await getSummary(gameKey);
		summary.destinations.sort((a, b) => a.index - b.index);
		console.log(summary);
		loading = false;
	};

	onMount(_loadGameSummary);
</script>

{#if loading}
	<Loading/>
{:else if summary}
	<div class="h-full flex flex-col">
		<Summary
			{summary}
			{userInGame}
			reloadGameSummary={_loadGameSummary}
		/>
	</div>
{:else}
	<div class="h-full flex flex-col">
		<h1 class="text-lg mt-4 text-center text-gray-700">
			No game summary found.
		</h1>
	</div>
{/if}