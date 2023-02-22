<script>
	import { onMount } from "svelte";
	import { buttonStyle, indigoStyle } from "../../../css";
    import { gamePage, groupStore, joinLobby } from "../../../stores";

    // onMount(() => {
    //     joinLobby();
    // });
</script>

<div class="mb-5">
    Game Lobby Page:
</div>

<button
    class="{buttonStyle} {indigoStyle}"
    on:click={() => gamePage.set('/game/map')}
>
    Start Game
</button>