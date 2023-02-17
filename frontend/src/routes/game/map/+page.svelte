<script>
	import { onMount } from 'svelte';
	import Map from './map.svelte';
    import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';

    let mounted = false;
    let ready = false;

    onMount(() => {
        window.initMap = () => ready = true;
        mounted = true;
    })
</script>

<svelte:head>
    {#if mounted}
        <script
            defer async
            src={`https://maps.googleapis.com/maps/api/js?key=${PUBLIC_GOOGLE_MAPS_API_KEY}&callback=initMap`}
        />
    {/if}
</svelte:head>

{#if ready}
    <Map/>
{/if}