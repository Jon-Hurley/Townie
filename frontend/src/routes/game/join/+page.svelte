<script>
    import { buttonStyle, blueStyle, indigoStyle, inputStyle } from '../../../css';
	import { gamePage, joinLobby } from '../../../stores';
    import { createLobby } from '../../../requests/group';

    let lobbyInput;

    const _joinLobby = async() => {
        await joinLobby(lobbyInput);
        gamePage.set('/game/lobby');
    };

    const _createLobby = async() => {
        const lobbyKey = await createLobby();
        if (!lobbyKey) return;
        await joinLobby(lobbyKey);
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