<script>
    import { buttonStyle, blueStyle, indigoStyle, inputStyle } from '../../../css';
    import { createGame } from '../../../requests/group';
    import { Game } from '../../../Game';
    import { goto } from '$app/navigation';
	
    let lobbyInput;

    const _joinLobby = async() => {
        const res = await Game.join(lobbyInput);
        console.log("Err:", res);
    };

    const _createLobby = async() => {
        const lobbyKey = await createGame();
        if (!lobbyKey) return;
        console.log("lobby created w/ key: ", lobbyKey);
        const res = await Game.join(lobbyKey);
        console.log("Err:", res);
        goto(Game.getPage()) // JON ADDED THIS
        
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