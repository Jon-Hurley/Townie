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
	import { pushPopup, userStore } from '../../../../stores';

    const gameStore = Game.store;
    const mapSettingsStore = Map.settings;
    const locationStore = Location.store;

    //let showDestination = false;

    let skipPopupOpen = false;
    let shrinkPopupOpen = false;
    let exactLocationPopupOpen = false;
    let errorPopupOpen = false;

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
        console.log("Current radius: " + Map.settings.destinationRadius);
        Map.updateExactLocation(x => false);
        Map.updateDestinationRadius(x => 1);
        Map.updateDestinationRadiusScalar(x => 1);
        console.log(Map.settings.destinationRadius);
        console.log("Exact location is: " + Map.settings.exactLocation);
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

    const peekAtLocation = async(pointsSpent) => {
        console.log("Peeking at location for " + pointsSpent + " points!")
        let user = get(userStore);
        console.log("Points spent before peek: " + user.points);

        user.points -= pointsSpent;

        let option = pointsSpent == 750 ? 0 : 1;

        let res = await spendPoints(option);
        if (!res) {
            return -1;
        }
        console.log("Points spent after peek: " + get(userStore).points);
        if (pointsSpent == 750) {
            console.log("we shrinkin")
            Map.updateDestinationRadiusScalar(x => x * 0.5);
            Map.updateDestinationRadius(x => x * Map.updateDestinationRadiusScalar);
            Map.setCenterToCurrent();
            Map.updateDestinationCircle();
            Map.updateBounds();
        } else {
            Map.settings.exactLocation = true;
            Map.setCenterToCurrent();
            Map.updateDestinationCircle();
            Map.updateBounds();
        }
        
        return 0;
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
{:else if shrinkPopupOpen}
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
                    Do you want to shrink the destination radius for 750 points?
                </p>
            </div>

            <div class="mr-2 ml-2 grid grid-cols-2 gap-4 flex items-center px-4 py-3">
                <div>
                    <button
                        id="cancel-btn"
                        on:click={() => {
                            shrinkPopupOpen = false;
                        }}
                        class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm hover:border-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
                    >
                        CANCEL
                    </button>
                </div>
                <div>
                    <button
                        id="skip-btn"
                        on:click={() => {
                            shrinkPopupOpen = false;
                            let res = peekAtLocation(750);
                            if (res == -1) {
                                pushPopup(0, 
                                "You don't have enough points to shrink the destination radius.",
                                () => {} );
                            }
                        }}
                        class="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
                    >
                        YES
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
{:else if exactLocationPopupOpen}
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
						Do you want to show the exact location for 1500 points?
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
							on:click={() => {
                                exactLocationPopupOpen = false;
                                let res = peekAtLocation(1500);
                                if (res == -1) {
                                    pushPopup(0, 
                                    "You don't have enough points to show the exact location.",
                                    () => {} );
                                }
                            }}
							class="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
						>
							Yes
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
			shrinkPopupOpen = true;
		}}
		name="shrinkRadiusButton"
		id="shrinkRadius-btn"
		class="{buttonStyle} {blueStyle} flex z-500"
	>
		<div class="px-4">Shrink Radius</div>
	</button>
    </div>
</div>

<div>
    <div class="flex flex-cols justify-center items-center">
        <button
		on:click={() => {
			exactLocationPopupOpen = true;
		}}
		name="showExactButton"
		id="showExact-btn"
		class="{buttonStyle} {blueStyle} flex z-500"
	>
		<div class="px-4">Show Exact Location</div>
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

    {#if Map.settings.destinationRadius < 0.1 || Map.settings.exactLocation}
        <Marker
            lng={Game.nextDestination.lon}
            lat={Game.nextDestination.lat}
            color="rgb(255,0,0)"
        />
    {/if}

    <Marker
        lng={$locationStore.lng}
        lat={$locationStore.lat}
        label={'You'}
        color="rgb(255,0,0)"
    />
</Mapbox>