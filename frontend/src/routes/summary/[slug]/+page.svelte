<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getSummary } from '../../../requests/search';
	import Loading from '../../../components/loading.svelte';
	import Summary from './summary.svelte';

	let summary;

	onMount(async () => {
		const gameKey = $page.params.slug;
		console.log($page);
		console.log({ gameKey });
		summary = await getSummary(gameKey);
	});
</script>

{#if summary}
	<div class="h-full flex flex-col">
		<Summary {summary} />
	</div>
{:else if summary === false}
	<div class="h-full flex flex-col">
		<h1 class="text-2xl mt-4 text-center text-gray-700">No game summary found.</h1>
	</div>
{:else}
	<Loading />
{/if}
