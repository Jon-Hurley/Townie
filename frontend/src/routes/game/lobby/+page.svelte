<script>
	import { onMount } from "svelte";
	import { buttonStyle, indigoStyle } from "../../../css";
    import { gamePage } from "../../../stores";

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