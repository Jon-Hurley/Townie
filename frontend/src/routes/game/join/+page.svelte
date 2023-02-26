<script>
    import { buttonStyle, blueStyle, indigoStyle, inputStyle } from '../../../css';
	import { gamePage, joinGame } from '../../../stores';
    import { createGame } from '../../../requests/group';
    import Dests from "./dests.svelte";

    let lobbyInput;

    const _joinLobby = async() => {
        const res = await joinGame(lobbyInput);
        if (!res) return;
        gamePage.set('/game/lobby');
    };

    const _createLobby = async() => {
        const lobbyKey = await createGame();
        if (!lobbyKey) return;
        console.log("lobby created w/ key: ", lobbyKey);
        const res = await joinGame(lobbyKey);
        if (!res) return;
        gamePage.set('/game/lobby');
    };
</script>

<div
    class="
        h-full
        flex flex-col justify-center items-center
    "
>
    <div
        class="
            flex flex-col justify-center items-center
            w-full h-full max-w-sm
        "
    >
        <input
            bind:value={lobbyInput}
            type="text"
            class="{inputStyle}"
            placeholder="Enter Lobby ID"
        />
        <button
            class="{buttonStyle} {indigoStyle} w-full mt-2"
            on:click={_joinLobby}
        >
            Join Lobby
        </button>
    </div>

    <button
        class="{buttonStyle} {blueStyle} w-full mt-4 max-w-sm"
        on:click={_createLobby}
    >
        Create Lobby
    </button>
</div>

<Dests/>