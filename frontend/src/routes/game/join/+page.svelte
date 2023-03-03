<script>
    import { buttonStyle, blueStyle, indigoStyle, inputStyle } from '../../../css';
    import { createGame, joinGame } from '../../../requests/group';
	import { subscribeLocationBeforeMap } from '../../../stores';

    let lobbyInput;

    const _joinLobby = async() => {
        const res = await joinGame(lobbyInput);
    };

    const _createLobby = async() => {
        const lobbyKey = await createGame();
        await subscribeLocationBeforeMap();
        if (!lobbyKey) return;
        console.log("lobby created w/ key: ", lobbyKey);
        const res = await joinGame(lobbyKey);
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
            w-full h-full
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
        class="{buttonStyle} {blueStyle} w-full mt-4"
        on:click={_createLobby}
    >
        Create Lobby
    </button>
</div>