<script>
	import '../app.css';
    import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';
    import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    
	import { mapStore, popupQueue, userStore } from '../stores';
    import { autoLogin } from '../requests/account';
    import Navbar from './navbar.svelte';
    import AccountBar from './account-bar.svelte';
	import Loading from '../general-components/loading.svelte';
	import Modal from '../general-components/modal.svelte';

	let mounted = false;
    let loaded = false;

    $: console.log({MAP: $mapStore})

	onMount(async () => {
        loaded = false;
        if (!$mapStore) {
            // create a function for the GOOGLE API to call when done initializing
            window.initMap = () => mapStore.set(true);
            mounted = true;
        }
        if (!$userStore) {
            const res = await autoLogin();
            if (!res) {
                goto('/login');
            }
        }
        loaded = true;
	});

	
	let lastState = false;
	$: {
        loaded = false;
        console.log('NEW USER: ', $userStore);
        if (lastState && !$userStore) { // IF user goes valid to invalid, GOTO login.
            goto('/login');
            console.log('User state set to null: GOTO LOGIN');
        }
        if (!lastState && $userStore) { // IF user goes invalid to valid, GOTO game.
            console.log('PAGE PATH: ', $page);
            if ($page.route.id === '/login' || $page.route.id === '/signup') {
                goto('/game');
                console.log('User state set to valid: GOTO GAME');
            }
            userStore.subscribe((user) => {
                if (user?.token) {
                    sessionStorage.setItem('token', user.token);
                }
            });
        }
		lastState = !!$userStore;
        loaded = true;
	}
    $: console.log({slots: $$slots})
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

{#if loaded}
    <div class="
        flex flex-col justify-between items-center
        h-screen w-screen max-h-screen max-w-screen
    ">
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
            <slot/>
        {/if}
    </div>
{:else}
    <Loading/>
{/if}

{#if $popupQueue.length}
    <Modal
        {...$popupQueue[0]}
    />
{/if}