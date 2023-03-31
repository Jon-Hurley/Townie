<script>
    import { userStore } from "../../stores";
    import { Game } from "../../classes/Game";
    import { Location } from "../../classes/Location";
    import { onMount } from 'svelte';
    import { updatePlayableGame } from "../../requests/account";
    import { createGame } from "../../requests/group";
    import { get } from 'svelte/store';
	import { blueStyle, buttonStyle } from "../../css";
    import { goto } from '$app/navigation';

    const currentTime = Math.floor(Date.now() / 1000)
    const user = get(userStore)
    let prevTime = user.nextAvailableGame;
    let playable = user.weeklyGamePlayed;
    let form = {};
    let display = {};
    const theme_options = ["Tourism", "Food", "Shopping", "Museum"];
    const budget_options = ["Free", "10", "25", "50", "Splurge!"];

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
                display.transportation = "Driving";
            }
            else if (transportation == 1) {
                form['drivingAllowed'] = false;
                form['walkingAllowed'] = true;
                form['transitAllowed'] = false;
                form['bicyclingAllowed'] = false;
                display.transportation = "Walking";
            }
            else if (transportation == 2) {
                form['drivingAllowed'] = false;
                form['walkingAllowed'] = false;
                form['transitAllowed'] = true;
                form['bicyclingAllowed'] = false;
                display.transportation = "Transit";
            }
            else if (transportation == 3) {
                form['drivingAllowed'] = false;
                form['walkingAllowed'] = false;
                form['transitAllowed'] = false;
                form['bicyclingAllowed'] = true;
                display.transportation = "Bicycling";
            }

            const desiredCompletionTimeMap = [ 30, 60, 90, 120, 180 ];
            form.desiredCompletionTime = desiredCompletionTimeMap[desiredCompletionTime];
            display.desiredCompletionTime = desiredCompletionTimeMap[desiredCompletionTime]; 
                        
            const themeMap = [ "tourist_attraction", "restaurant", "store", "museum" ];
            form.theme = themeMap[theme];
            display.theme = theme_options[theme]; 

            const radiusMap = [ 1, 2, 5, 10, 15, 20, 25 ];
            form.radius = radiusMap[radius];
            display.radius = radiusMap[radius];

            form.budget = budget;
            display.budget = budget_options[budget];
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
        const loc = await Location.getCurrentLocation();
        form.lat = loc.lat;
        form.lon = loc.lng;
        await Game.updateSettings(form);
        console.log(Game.game)
        goto('/game')
    }
</script>

{#if (currentTime - prevTime > 604800)}
    <div class="flex">
        <ul bind:this={display}
            class=" {buttonStyle} {blueStyle} w-full"
        >
            <li>Theme: {display.theme}</li>
            <li>Length: {display.desiredCompletionTime} minutes</li>
            <li>Radius: {display.radius}</li>
            <li>Transportation: {display.transportation}</li>
            <li>Budget Per Attraction: {display.budget} </li>
            
        </ul>
    </div>
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