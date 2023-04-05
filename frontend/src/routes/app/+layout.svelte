<script>
    import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';
    import { onMount } from 'svelte';

    import Navbar from '../app/navbar.svelte';
    import AccountBar from '../app/account-bar.svelte';
	import Loading from '../../general-components/loading.svelte';
  
	import { mapStore, userStore } from '../../stores';

	let mounted = false;
    let loaded = false;

	onMount(async () => {
        loaded = false;
        if (!$mapStore) {
            // create a function for the GOOGLE API to call when done initializing
            window.initMap = () => mapStore.set(true);
            mounted = true;
        }
        userStore.subscribe(user => {
            if (user?.token) {
                sessionStorage.setItem('token', user.token);
            }
        });
        loaded = true;
	});

    $: if (!$userStore) goto('/login');
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

{#if $userStore}
    <AccountBar/>
    <div
        class="
            m-0 p-4 h-full
            h-screen w-screen max-h-screen max-w-screen
        "
    >
        <slot/>
    </div>
    <Navbar/>
{:else}
    <Loading/>
{/if}