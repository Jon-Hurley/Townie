<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getSummary } from '../../../requests/search';
	import Loading from '../../../components/loading.svelte';
	import Summary from './summary.svelte';

	let summary;

	onMount(async () => {
		const id = $page.params.slug;
		summary = await getSummary(id);
	});
</script>

{#if summary}
	<div class="h-full flex flex-col">
		<Summary {summary} />
	</div>
{:else}
	<Loading />
{/if}
