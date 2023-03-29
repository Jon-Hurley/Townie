<script>
    import { buttonStyle, indigoStyle, redStyle } from '../../css';
	import { Game } from '../../classes/Game';
	import Settings from './settings.svelte';
	import Leaderboard from './leaderboard.svelte';

    const gameStore = Game.store;
    $: gamePage = $gameStore?.game?.page || 'join';

    const _leaveGame = async () => {
		let res = await Game.leave();
	};

    const _startGame = async() => {
        const err = Game.start();
        if (err) {
            messageObj = {
                status: 0,
                message: err,
                dest: null
            }
            return;
        }
    }
</script>

<div class="flex w-full justify-between mt-4 gap-2">
    <!-- {#if gamePage === 'map'} -->
        <Leaderboard/>
    <!-- {/if} -->

    <Settings/>

    <button
        on:click={_leaveGame}
        class="{buttonStyle} {redStyle}"
    >
        Leave
    </button>

    {#if gamePage === 'lobby'}
        <button
            class="{buttonStyle} {indigoStyle} w-24"
            on:click={_startGame}
        >
            Start
        </button>     
    {/if}
</div>