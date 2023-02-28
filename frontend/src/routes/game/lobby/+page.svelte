<script>
    import { onMount } from "svelte";
    import { groupStore, userStore } from "../../../stores";
    onMount(async() => {
        console.log(userStore.username == '')
        if (userStore.username == '') {
			goto('user/login')
		}
    });
</script>

<div class="mb-5">
    Game Lobby Page:
</div>

<a href="/game/map">
    <button class="border p-2 rounded-md">
        Go to /game/map
    </button>
</a>