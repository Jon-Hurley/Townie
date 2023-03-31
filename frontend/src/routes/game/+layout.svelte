<script>
    import { Game } from '../../classes/Game';
	import Loading from '../../general-components/loading.svelte';
	import { mapStore } from '../../stores';
    import Join from './join/join.svelte';
	import Lobby from './lobby/lobby.svelte';
	import Map from './map/map.svelte';
	import Subnav from './subnav.svelte';
    
    let gameStore = Game.store;    
    $: gamePage = $gameStore?.game?.page || 'join';
    let loading = false;

    const _leaveGame = async () => {
		let res = Game.leave();
	};
    const _startGame = async() => {
        loading = true;
        const success = await Game.start();
        loading = false;
    }
</script>

{#if loading}
    <Loading/>
{:else}
    <div class="flex flex-col h-full">
        {#if gamePage === 'join'}
            <Join/>
        {:else if gamePage === 'lobby'}
            <Lobby/>
        {:else if gamePage === 'map'}
            {#if $mapStore}
                <Map/>
            {:else}
                <Loading/>
            {/if}
        {/if}
        <Subnav
            startGame={_startGame}
            leaveGame={_leaveGame}
            gamePage={gamePage}
        />
    </div>
{/if}