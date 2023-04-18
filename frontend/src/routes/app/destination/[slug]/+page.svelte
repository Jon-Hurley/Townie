<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	import Loading from '../../../../general-components/loading.svelte';
	import Destination from './destination.svelte';

	import { getDestination } from '../../../../requests/search';

	let data;
	let loading = false;

	const _getDestination = async () => {
		loading = true;
		const destKey = $page.params.slug;
		data = await getDestination(destKey);
		console.log(data)
		loading = false;
	};

	onMount(_getDestination);
</script>

{#if loading}
	<Loading />
{:else if data}
	<div class="h-full flex flex-col">
		<Destination
			destination={data.destination}
			theme={data.theme}
			userRating={data.userRating}
			reload={_getDestination}
		/>
	</div>
{:else}
	<div class="mt-4 flex justify-center">
		No game summary found.
	</div>
{/if}