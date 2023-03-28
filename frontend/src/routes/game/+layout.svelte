<script>
    import { Game } from '../../classes/Game';
    import Modal from '../../general-components/modal.svelte';
	import Join from './join/join.svelte';
	import Lobby from './lobby/lobby.svelte';
    
    let gameStore = Game.store;
    let gameMessageObj = Game.messageObj;

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
{:else if gamePage === 'game'}
    <slot name="game">
        <Game/>
    </slot>
{:else if gamePage === 'summary'}
    <slot name="summary"/>
{/if}