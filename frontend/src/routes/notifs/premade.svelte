<script>
    import { userStore } from "../../stores";
    import { Game } from "../../Game";
    import { onMount } from 'svelte';
    import { updatePlayableGame } from "../../requests/account";
    import { createGame } from "../../requests/group";
    import { goto } from '$app/navigation';
    import { get } from 'svelte/store';

    const currentTime = Math.floor(Date.now() / 1000)
    const user = get(userStore)
    let prevTime = user.next_available_game;
    let playable = user.weekly_game_played;
    let form = {};

    let yes = false;

    const _updatePlayable = async() => {
        updatePlayableGame(true, Math.floor(Date.now() / 1000))
        const lobbyKey = await createGame();
        if (!lobbyKey) return;
        console.log("lobby created w/ key: ", lobbyKey);
        const res = await Game.join(lobbyKey);
        console.log("Err:", res);
        Game.updateSettings(form);
        console.log(Game.store)
        //goto(Game.getPage()) // JON ADDED THIS
    }

    onMount(() => {
        Game.store.subscribe(gs => {
            if (gs) {
                form = { ...gs.game.settings };
                form.otherCompletionTime = form.otherCompletionTime;
                form.otherRadius = form.otherRadius;
                form.otherBudget = form.otherBudget;
            }
        })
        if (!playable || currentTime - prevTime < 604800) {
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

            if (desiredCompletionTime == 0) {
                form.desiredCompletionTime = 30;
            }
            else if (desiredCompletionTime == 1) {
                form.desiredCompletionTime = 60;
            }
            else if (desiredCompletionTime == 2) {
                form.desiredCompletionTime = 90;
            }
            else if (desiredCompletionTime == 3) {
                form.desiredCompletionTime = 120;
            }
            else if (desiredCompletionTime == 4) {
                form.desiredCompletionTime = 180;
            }

            if (theme == 0) {
                form.theme = "tourist_attraction";
            }
            else if (theme == 1) {
                form.theme = "restaurant";
            }
            else if (theme == 2) {
                form.theme = "store";
            }
            else if (theme == 3) {
                form.theme = "museum";
            }

            if (radius == 0) {
                form.radius = 1;
            }
            else if (radius == 1) {
                form.radius = 2;
            }
            else if (radius == 2) {
                form.radius = 5;
            }
            else if (radius == 3) {
                form.radius = 10;
            }
            else if (radius == 4) {
                form.radius = 15;
            }
            else if (radius == 5) {
                form.radius = 20;
            }
            else if (radius == 6) {
                form.radius = 25;
            }

            form.budget = budget;
            console.log(form)
        }
    })



</script>
{#if (currentTime - prevTime < 604800)}
<div class="flex ">
    <button
        on:click={() => {
            _updatePlayable()
        }}
    >
        Create premade lobby!
    </button>
</div>
{/if}