<script>
    import { buttonStyle, inputStyle } from '../../../../css';
    import { createGame } from '../../../../requests/group';
    import { Game } from '../../../../classes/Game';
	import Loading from '../../../../general-components/loading.svelte';
	import { primaryColor } from '../../../../stores';
    import Logo from '$lib/assets/townie-Full-Logo.jpg';
    import Skyline from '$lib/assets/Logo-Skyline.png';
    import Premade from './premade.svelte';

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
        loading = false;
    };
</script>

{#if loading}
    <Loading/>
{:else}
    <img
        src="{Logo}"
        alt="Townie Logo"
        class ="rounded-md shadow-sm"
        style="width: full height: 200px"
    >
    <div
        class="
            flex flex-col justify-center items-center
            w-full mt-4
        "
    >
        <button
            class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 w-full"
            on:click={_createLobby}
        >
            Create Lobby
        </button>
        <div
            class="
                flex flex-col justify-center items-center
                w-full h-1/2 my-14
            "
        >
            <input
                bind:value={lobbyInput}
                type="text"
                class="{inputStyle} focus:ring-{$primaryColor}-500"
                placeholder="Enter Lobby ID"
            />
            <button
                class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 w-full mt-2"
                on:click={_joinLobby}
            >
                Join Lobby
            </button>
        </div>
        <Premade/>
    </div>
    <div
        class="absolute inset-x-0 bottom-14 rounded-md shadow-sm"
        style="
            background-image: url({Skyline});
            width: full;
            height: 200px;
            background-size: cover;
            radius: 8px 8px 50% 50%;
            ">
    </div>
{/if}