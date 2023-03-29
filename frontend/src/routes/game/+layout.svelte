<script>
    import { Game } from '../../classes/Game';
	import Loading from '../../general-components/loading.svelte';
    import Join from './join/join.svelte';
	import Lobby from './lobby/lobby.svelte';
	import Map from './map/map.svelte';
    
    let gameStore = Game.store;
    
    $: gamePage = $gameStore?.game?.page || 'join';
</script>

{#if gamePage === 'join'}
    <slot name="join">
        <Join/>
    </slot>
{:else if gamePage === 'lobby'}
    <slot name="lobby">
        <Lobby/>
    </slot>
{:else if gamePage === 'map'}
    <slot name="map">
        <Map/>
    </slot>
{:else if gamePage === 'summary'}
    <slot name="summary">
    </slot>
{:else}
    <Loading/>
{/if}