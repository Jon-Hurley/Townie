<script>
	import '../app.css';
	import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { gameStore, mapStore, userStore } from '../stores';
	import { autoLogin } from '../requests/account';
	import Navbar from '../components/navbar.svelte';
	import AccountBar from '../components/account-bar.svelte';

	let mounted = false;
	mapStore.set(false);

	onMount(async () => {
		// create a function for the GOOGLE API to call when done initializing
		window.initMap = () => mapStore.set(true);
		mounted = true;

		const res = await autoLogin();
		if (!res) {
			goto('/login');
		}
	});

	// IF user goes valid to invalid, GOTO login.
	let lastState = false;
	$: {
		console.log('NEW USER: ', $userStore);
		if (lastState && !$userStore) goto('/login');
		if (!lastState && $userStore) {
			if ($page.path === '/login' || $page.path === '/signup') goto('/account');
		}
		lastState = !!$userStore;
	}
</script>

<!-- Once mounted, bring in the GOOGLE API -->
<svelte:head>
	{#if mounted}
		<script
			defer
			async
			src={`https://maps.googleapis.com/maps/api/js?key=${PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=places&callback=initMap`}
		></script>
	{/if}
</svelte:head>

<div class="flex flex-col justify-between items-center h-screen w-screen">
	{#if $userStore}
		<AccountBar />
		<div class="m-0 w-full p-4 h-full">
			<slot />
		</div>
		<Navbar />
	{:else}
		<slot />
	{/if}
</div>
