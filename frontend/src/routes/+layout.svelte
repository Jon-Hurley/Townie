<script>
	import '../app.css';
    import Navbar from '../components/navbar.svelte';
    import AccountBar from '../components/account-bar.svelte';

    import { onMount } from 'svelte';
    import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';
	import { mapStore } from '../stores';

    let mounted = false;
    mapStore.set(false);

    onMount(() => {
        // create a function for the GOOGLE API to call when done initializing
        window.initMap = () => mapStore.set(true);
        mounted = true;
    })
</script>

<!-- Once mounted, bring in the GOOGLE API -->
<svelte:head>
    {#if mounted}
        <script
            defer async
            src={`https://maps.googleapis.com/maps/api/js?key=${PUBLIC_GOOGLE_MAPS_API_KEY}&callback=initMap`}
        />
    {/if}
</svelte:head>


<AccountBar/>
<div
    class="m-0 w-full p-4"
    style="height: calc(100vh - 120px);"
>
    <slot/>
</div>
<Navbar/>