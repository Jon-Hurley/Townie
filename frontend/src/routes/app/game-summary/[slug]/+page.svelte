<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	import Loading from '../../../../general-components/loading.svelte';
	import Summary from './summary.svelte';

	import { getSummary } from '../../../../requests/search';
	import { userStore } from '../../../../stores';
	
	let loading = false;

	let summary;
	$: userInGame = !!summary?.players?.find(x => x?.username == $userStore.username);

	const _loadGameSummary = async () => {
		loading = true;
		const gameKey = $page.params.slug;
		summary = await getSummary(gameKey);
		summary?.destinations.sort((a, b) => a.index - b.index);
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
	<div class="mt-4 flex justify-center">
		No game summary found.
	</div>
{/if}