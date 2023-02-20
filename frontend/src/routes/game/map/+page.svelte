<script>
	import Map from './map.svelte';
    import { mapStore } from '../../../stores';

    mapStore.subscribe((v) => console.log(v))
</script>

{#if $mapStore}
    <Map/>
{/if}