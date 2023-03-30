<script>
	import { mapStore } from '../../../stores';
	import GameMap from './gameMap.svelte';
</script>

{#if $mapStore}
    <GameMap/>
{/if}

