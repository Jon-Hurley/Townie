<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getSummary } from '../../../requests/search';
	import Loading from '../../../components/loading.svelte';
	import Summary from './summary.svelte';

	let summary;

	onMount(async () => {
		const key = $page.params.slug;
		summary = await getSummary(key);
	});
</script>

{#if summary}
	<div class="h-full flex flex-col">
		<Summary {summary} />
	</div>
{:else if summary === 0}
	<div class="h-full flex flex-col">
		<h1 class="text-2xl text-center">No game summary found</h1>
	</div>
{:else}
	<Loading />
{/if}
