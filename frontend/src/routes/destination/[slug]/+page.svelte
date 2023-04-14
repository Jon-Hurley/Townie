<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getDestination } from '../../../requests/search';
	import { rating } from '../../../requests/search';
	import { userStore } from '../../../stores';
	import Loading from '../../../general-components/loading.svelte';
	import Destination from './destination.svelte';

	let ratings;
	let destination;

	onMount(async () => {
		let destKey = $page.params.slug;
		if (!destKey) {
			const url = window.location.href;
			destKey = url.substring(url.lastIndexOf('/') + 1);
		}

		destination = await getDestination(destKey);

		console.log(destination);
	});
</script>

{#if destination}
	<div class="h-full flex flex-col">
		<Destination {destination} />
	</div>
{:else if destination === false}
	<div class="h-full flex flex-col">
		<h1 class="text-2xl mt-4 text-center text-gray-700">No game destination found.</h1>
	</div>
{:else}
	<Loading />
{/if}
