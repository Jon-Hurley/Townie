<script>
    import { Game } from '../../classes/Game';
	import { buttonStyle, redStyle } from '../../css';
    import Modal from '../../general-components/modal.svelte';
	import Join from './join/join.svelte';
	import Lobby from './lobby/lobby.svelte';
	import Map from './map/map.svelte';
    
    let gameStore = Game.store;
    let gameMessageObj = Game.messageObj;

    const _leaveGame = async () => {
		let res = await Game.leave();
	};
    
    $: gamePage = $gameStore?.game?.page || 'join';
</script>

<Modal
	{...$gameMessageObj}
/>

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
{/if}