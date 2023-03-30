<script>
	import { mapStore } from '../../../stores';
	import Timer from '../timer.svelte';
	import GameMap from './gameMap.svelte';
</script>

{#if $mapStore}
    <GameMap/>
	<Timer/>
{/if}