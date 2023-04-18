<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	import Loading from '../../../general-components/loading.svelte';
	import Destination from './destination.svelte';

	import { getDestination } from '../../../requests/search';

	let destination;
	let loading = false;

	const _getDestination = async () => {
		loading = true;
		const destKey = $page.params.slug;
		destination = await getDestination(destKey);
		console.log(destination);
		loading = false;
	};

	onMount(_getDestination);
</script>

{#if destination}
	<div class="h-full flex flex-col">
		<Destination {destination} />
	</div>
{:else if destination === false}
	<div class="h-full flex flex-col">
		<h1 class="text-2xl mt-4 text-center text-gray-700">
			No game destination found.
		</h1>
	</div>
{:else}
	<Loading />
{/if}