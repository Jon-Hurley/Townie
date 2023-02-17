<script>
	import { onDestroy, onMount } from 'svelte';
	import Map from './map.svelte';
    import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';
	import { mapStore } from '../../../stores';

    mapStore.subscribe((v) => console.log(v))
</script>

{#if $mapStore}
    <Map/>
{/if}