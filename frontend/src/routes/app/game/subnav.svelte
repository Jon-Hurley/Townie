<script>
    import { buttonStyle, hr, indigoStyle, redStyle } from '../../../css';

    import Leaderboard from './leaderboard.svelte';
	import MapSettings from './map/mapSettings.svelte';
	import LobbySettings from './lobby/lobbySettings.svelte';
	import Chat from './chat.svelte';
    import Locations from './locations.svelte'
    import { Game } from '../../../classes/Game';
    const gameStore = Game.store;

    export let startGame, leaveGame, gamePage;    
</script>

{#if $gameStore}
    <hr class={hr}>
    <div
        class="
            flex
            w-full justify-between
            pt-4 gap-2
            z-50
        "
    >
        <Chat/>

        {#if gamePage === 'map'}
            {#if $gameStore.game.settings.casual}
                <Locations/>
            {:else}
                <Leaderboard/>
            {/if}
        {/if}

        {#if gamePage === 'lobby'}
            <LobbySettings/>
        {:else}
            <MapSettings/>
        {/if}

        <button
            on:click={leaveGame}
            class="{buttonStyle} {redStyle}"
        >
            Leave
        </button>

        {#if gamePage === 'lobby'}
            <button
                class="{buttonStyle} {indigoStyle} w-24"
                on:click={startGame}
            >
                Start
            </button>     
        {/if}
    </div>
{/if}