<script>
	import Map from './map.svelte';
    import { mapStore } from '../../../stores';
</script>

{#if $mapStore}
    <Map/>
{/if}