<script>
    import { userStore } from "../../stores";
    import { Game } from "../../classes/Game";
    import { onMount } from 'svelte';
    import { updatePlayableGame } from "../../requests/account";
    import { createGame } from "../../requests/group";
    import { get } from 'svelte/store';
	import { blueStyle, buttonStyle } from "../../css";

    const currentTime = Math.floor(Date.now() / 1000)
    const user = get(userStore)
    let prevTime = user.next_available_game;
    let playable = user.weekly_game_played;
    let form = {};

    let yes = false;

    onMount(() => {
        if (!playable || currentTime - prevTime > 604800) {
            let transportation = Math.floor(Math.random() * 4);
            let desiredCompletionTime = Math.floor(Math.random() * 5);
            let theme = Math.floor(Math.random() * 4)
            let radius = Math.floor(Math.random() * 7);
            let budget = Math.floor(Math.random() * 5);
            
            if (transportation == 0) {
                form['drivingAllowed'] = true;
                form['walkingAllowed'] = false;
                form['transitAllowed'] = false;
                form['bicyclingAllowed'] = false;
            }
            else if (transportation == 1) {
                form['drivingAllowed'] = false;
                form['walkingAllowed'] = true;
                form['transitAllowed'] = false;
                form['bicyclingAllowed'] = false;
            }
            else if (transportation == 2) {
                form['drivingAllowed'] = false;
                form['walkingAllowed'] = false;
                form['transitAllowed'] = true;
                form['bicyclingAllowed'] = false;
            }
            else if (transportation == 3) {
                form['drivingAllowed'] = false;
                form['walkingAllowed'] = false;
                form['transitAllowed'] = false;
                form['bicyclingAllowed'] = true;
            }

            const desiredCompletionTimeMap = [ 30, 60, 90, 120, 180 ];
            form.desiredCompletionTime = desiredCompletionTimeMap[desiredCompletionTime];
                        
            const themeMap = [ "tourist_attraction", "restaurant", "store", "museum" ]
            form.theme = themeMap[theme];

            const radiusMap = [ 1, 2, 5, 10, 15, 20, 25 ];
            form.radius = radiusMap[radius];

            form.budget = budget;
            console.log(form)
        }
    })

    const _updatePlayable = async() => {
        updatePlayableGame(true, Math.floor(Date.now() / 1000))
        const lobbyKey = await createGame();
        if (!lobbyKey) return;
        
        console.log("lobby created w/ key: ", lobbyKey);
        const res = await Game.join(lobbyKey);
        console.log("Err:", res);
        Game.updateSettings(form);
    }
</script>

{#if (currentTime - prevTime > 604800)}
    <div class="flex ">
        <button
            on:click={() => {
                _updatePlayable()
            }}
            class="{buttonStyle} {blueStyle} w-full"
        >
            Create premade lobby!
        </button>
    </div>
{/if}