<script>
	import Map from './map.svelte';
    import { joinLobby, mapStore } from '../../../stores';
	import { onMount } from 'svelte';

    mapStore.subscribe((v) => console.log(v))

    
</script>

{#if $mapStore}
    <Map/>
{/if}