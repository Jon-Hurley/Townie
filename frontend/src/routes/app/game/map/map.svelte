<script>
	import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';
    import { onDestroy, onMount } from 'svelte';
    import { Map as Mapbox, Marker } from '@beyonk/svelte-mapbox';
    import { buttonStyle, blueStyle } from '../../../../css';
    import * as turf from '@turf/turf';
    import { get } from 'svelte/store';

    import Timer from './timer.svelte';
    import Options from './options.svelte';

    import { Location } from '../../../../classes/Location';
    import { Map } from '../../../../classes/Map';
    import { Game } from '../../../../classes/Game';
    import { spendPoints } from '../../../../requests/account';
	import { incrementDestinationIndex } from '../../../../requests/search';
	import { userStore } from '../../../../stores';

    const gameStore = Game.store;
    const mapSettingsStore = Map.settings;
    const locationStore = Location.store;

    let shrinkFactor = 1;
    let showDestination = false;

    let skipPopupOpen = false;

    let tempText = (Game.player.destinationIndex === Game.destinations.length - 1) ? "WARNING: This is the final destination! If you skip this, you will be sent to the game summary page!" : "Do you want to skip this destination? If you do, you will not gain points for this destination."; 

    const onMapReady = async() => {
        const mapboxObj = Map.map.getMap();
        Map.setCenterToCurrent();
        Map.setDestinationCircle();
        // mapboxObj.setStyle('mapbox://styles/arnavmehra/cle7jp4jn003b01ntixmh28ea');
        gameStore.subscribe(Map.updateDestinationCircle);
        locationStore.subscribe(Map.updateBounds); 
    }

    onMount(() => {
        Location.subscribe();
    });

    onDestroy(() => {
        Location.unsubscribe();
        // Map.cancelSnapLocation();
    });

    const _skipLocation = () => {
        skipPopupOpen = false;
        if (Game.player.destinationIndex === Game.destinations.length - 1) {
            Game.leave();
            return;
        }
        console.log(Game.player.connectionId);
        incrementDestinationIndex(Game.player.connectionId);
        Game.player.destinationIndex++;
        Map.setCenterToCurrent();
        Map.updateDestinationCircle();
        Map.updateBounds();
        tempText = (Game.player.destinationIndex === Game.destinations.length - 1) ? "WARNING: This is the final destination! If you skip this, you will be sent to the game summary page!" 
                    : "Do you want to skip this destination? If you do, you will not gain points for this destination.";
    }

    const peekAtLocation = (pointsSpent) => {
        let user = get(userStore);
        if (pointsSpent > user.points) {
            alert("You don't have enough points to peek at this location!");
            return;
        }
        console.log("Points spent before peek: " + user.points);
        user.points -= pointsSpent;
        userStore.set(user);
        spendPoints(pointsSpent);
        console.log("Points spent after peek: " + get(userStore).points);
        //Map.setCenterToCurrent();
        //Map.updateDestinationCircle();
        //Map.updateBounds();
    }

</script>

<Timer/>

{#if skipPopupOpen}
	<!--skipLocation popup-->
	<div
		class="z-50 fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full "
		id="skipLocation-popup"
	>
		<div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-md bg-white">
			<div class="mt-3 text-center">
				<div class="mx-auto flex items-center justify-center rounded-full">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-12 h-12 text-red-600"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<h3 class="text-lg leading-6 font-medium text-gray-900">Are you sure?</h3>
				<div class="px-7 py-3">
					<p class="text-sm text-gray-500">
						{tempText}
					</p>
				</div>

				<div class="mr-2 ml-2 grid grid-cols-2 gap-4 flex items-center px-4 py-3">
					<div>
						<button
							id="cancel-btn"
							on:click={() => {
								skipPopupOpen = false;
							}}
							class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm hover:border-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
						>
							CANCEL
						</button>
					</div>
					<div>
						<button
							id="skip-btn"
							on:click={_skipLocation}
							class="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
						>
							SKIP
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}

<Options/>

<div>
    <div class="flex flex-cols justify-center items-center">
        <button
		on:click={() => {
			skipPopupOpen = true;
		}}
		name="skipLocationButton"
		id="skipLocation-btn"
		class="{buttonStyle} {blueStyle} flex z-500"
	>
		<div class="px-4">Skip Location</div>
	</button>
    </div>
</div>

<div>
    <div class="flex flex-cols justify-center items-center">
        <button
		on:click={() => {
			popupOpen = true;
		}}
		name="skipLocationButton"
		id="skipLocation-btn"
		class="{buttonStyle} {blueStyle} flex z-500"
	>
		<div class="px-4">Skip Location</div>
	</button>
    </div>
</div>

<Mapbox
    accessToken={PUBLIC_MAPBOX_TOKEN}
    bind:this={Map.map}
    on:ready={onMapReady}
    zoom={$mapSettingsStore.zoom}
>
    {#each $gameStore.players as player}
        {#if player.username !== $gameStore.player.username
             && player.lat !== null && player.lon !== null}
            <Marker
                lng={player.lon}
                lat={player.lat}
                color="rgb(255,0,0)"
            />
        {/if}
    {/each}

    <Marker
        lng={$locationStore.lng}
        lat={$locationStore.lat}
        label={'You'}
        color="rgb(255,0,0)"
    />
</Mapbox>