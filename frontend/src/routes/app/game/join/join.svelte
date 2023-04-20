<script>
    import { buttonStyle, blueStyle, indigoStyle, inputStyle } from '../../../../css';
    import { createGame } from '../../../../requests/group';
    import { Game } from '../../../../classes/Game';
	import Loading from '../../../../general-components/loading.svelte';
	
    let lobbyInput;
    let loading = false;

    const _joinLobby = async() => {
        loading = true;
        const res = await Game.join(lobbyInput);
        console.log("Success:", res);
        loading = false;
    };

    const _createLobby = async() => {
        loading = true;
        const lobbyKey = await createGame();
        if (!lobbyKey) return;
        console.log("lobby created w/ key: ", lobbyKey);
        const res = await Game.join(lobbyKey);
        console.log("Err:", res);
        loading = false;
    };
</script>

{#if loading}
    <Loading/>
{:else}
    <div
        class="
            flex flex-col justify-center items-center
            h-full
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
{/if}