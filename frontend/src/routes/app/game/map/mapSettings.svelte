<script>
	import { blueStyle, buttonStyle, grayStyle, hr, largeTitle } from '../../../../css';
	import { Game } from '../../../../classes/Game';
	import { Map } from '../../../../classes/Map';
	import { Location } from '../../../../classes/Location'; 
	import { pushPopup, userStore } from '../../../../stores';
	import { get } from 'svelte/store';
	import * as turf from '@turf/turf';
	import { spendPoints } from '../../../../requests/account';
	import { incrementDestinationIndex } from '../../../../requests/search';

	const settingsStore = Map.settings;

    let gameStore = Game.store;
	let form = {
        ...$gameStore.game.settings
    };
	let distanceStore = Game.distanceStore;

	let otherCompletionTime = false;
	let isOpen = false;

	let skipPopupOpen = false;
    let shrinkPopupOpen = false;
    let exactLocationPopupOpen = false;
    let errorPopupOpen = false;

	let tempText = (Game.player.destinationIndex === Game.destinations.length - 1) ? "WARNING: This is the final destination! If you skip this, you will be sent to the game summary page!" : "Do you want to skip this destination? If you do, you will not gain points for this destination."; 

	const _updateSettings = () => {
		Game.updateTime(form);
	};
	// let currLat;
	// let currLng;
	// let destLat;
	// let destLng;
	let exportNav;
	let url;
	// let from;
	// let to;
	const options = {units: 'degrees'};
	const _getNavigation = () => {
		console.log("Getting navigation");
		const currLat = Location.lat;
		const currLng = Location.lng;
		const destLat = Game.nextDestination.lat;
		const destLng = Game.nextDestination.lon;
		const from = turf.point([currLng, currLat]);
		const to = turf.point([destLng, destLat]);
		const distance = turf.distance(from, to, options);
		const addLat = Math.random();

		const randPos = (Math.random() * distance / 2.0);
		console.log(randPos);
		let finalLat;
		if (addLat > 0.5) {
			finalLat = destLat + randPos;
			console.log("added")
			console.log(finalLat);
		} else {
			finalLat = destLat - randPos;
			console.log("subtracted");
			console.log(finalLat);
		}
		
		exportNav = finalLat + "," + destLng;
		url = "https://www.google.com/maps/dir/?api=1&dir_action=navigate&destination=" + exportNav;
		window.open(url, "_blank");
	}

	const _getAccurateNavigation = () => {
		console.log("Getting accurate navigation");
		const currLat = Location.lat;
		const currLng = Location.lng;
		const destLat = Game.nextDestination.lat;
		const destLng = Game.nextDestination.lon;
		const from = turf.point([currLng, currLat]);
		const to = turf.point([destLng, destLat]);
		const distance = turf.distance(from, to, options);
		const addLat = Math.random();

		const randPos = (Math.random() * distance / 50.0);
		let finalLat;
		if (addLat > 0.5) {
			finalLat = destLat + randPos;
			console.log(finalLat);
		} else {
			finalLat = destLat - randPos;
			console.log(finalLat);
		}

		// const finalLat = Game.nextDestination.lat;
		// const destLng = Game.nextDestination.lon;
		
		exportNav = finalLat + "," + destLng;
		url = "https://www.google.com/maps/dir/?api=1&dir_action=navigate&destination=" + exportNav;
		window.open(url, "_blank");
	}

	const _skipLocation = () => {
        Map.updateDestinationRadiusScalar(x => 1);
		Game.handleRadiusUpdate();

        skipPopupOpen = false;
		isOpen = false;
        if (Game.player.destinationIndex === Game.destinations.length - 1) {
            Game.leave();
            return;
        }
        console.log(Game.player.connectionId);
        incrementDestinationIndex(Game.player.connectionId);
        Game.player.destinationIndex++;
		Game.formatStore.set(Game.updateDestTime());
		distanceStore.set(Game.updateDistance());
        Map.setCenterToCurrent();
        Map.updateDestinationCircle();
        Map.updateBounds();
        tempText = (Game.player.destinationIndex === Game.destinations.length - 1) ? "WARNING: This is the final destination! If you skip this, you will be sent to the game summary page!" 
                    : "Do you want to skip this destination? If you do, you will not gain points for this destination.";
    }

    const spendPointsHere = async(pointsSpent) => {
        let user = get(userStore);

        //let option = pointsSpent == 750 ? 0 : 1;
		let option = 0;
		if (pointsSpent == 750) {
			option = 0;
		} else if (pointsSpent == 1500) {
			option = 1;
		} else if (pointsSpent == 1750) {
			option = 2;
		}

        let success = await spendPoints(option);
        if (!success) {
            return -1;
        }
		user.points -= pointsSpent;
        if (pointsSpent == 750) {
			isOpen = false;
            Map.updateDestinationRadiusScalar(x => x * 0.5);
			console.log($settingsStore.destinationRadiusScalar);
            Map.setCenterToCurrent();
            Map.updateDestinationCircle();
            Map.updateBounds();
        } else if (pointsSpent == 1500) {
			isOpen = false;
            Map.updateDestinationRadiusScalar(x => 0);
            Map.setCenterToCurrent();
            Map.updateDestinationCircle();
            Map.updateBounds();
        } else {
			_getAccurateNavigation();
		}
        
        return 0;
    }
</script>

<button type="button" class="{buttonStyle} {grayStyle} w-full" on:click={() => (isOpen = true)}>
	Options
</button>

<div
	class="
        fixed inset-0 bg-gray-200 mb-16
        pointer-events-none
        transition-all duration-500
        {isOpen ? 'bg-opacity-75' : 'bg-opacity-0'}
    "
/>

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
                            let res = spendPointsHere(750);
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
								exactLocationPopupOpen = false;
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
                                let res = spendPointsHere(1500);
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
{/if}

<div
	class="
        fixed left-0 bottom-16
        w-screen text-center
        transition-all duration-500
        {isOpen ? 'translate-y-0' : 'translate-y-full pointer-events-none'}
    "
>
	<div
		class="
            bg-gray-50 p-4 rounded-t-lg
            w-full gap
        "
	>
		<div class={largeTitle}>Options</div>
		<hr class="{hr} my-4" />

		<div
			class="
                flex justify-between items-center
                bg-white p-3 mb-2 
                border-2 border-gray-200 rounded
            "
		>
			<div class="font-semibold">Length</div>
			<select
				on:change={(e) => {
					const v = e.target.value;
					otherCompletionTime = v === 'Other';
					if (!otherCompletionTime) {
						form.desiredCompletionTime = parseInt(v);
					}
				}}
				value={form.desiredCompletionTime}
				class="w-40"
			>
				{#each [30,60,90,120,180] as v}
					<option value={v}>{v} minutes</option>
				{/each}
				<option value="Other">Other</option>
			</select>

			{#if otherCompletionTime}
				<input
					class="w-40"
					placeholder="Other"
					type="number"
					min="1"
					value={form.desiredCompletionTime}
					on:input={(e) => {
						let v;
						try {
							v = parseInt(e.target.value);
						} catch (err) {
							v = 0;
						}
						form.desiredCompletionTime = Math.abs(v);
					}}
				/>
			{/if}
		</div>

		<hr class="{hr} my-4" />

		<div class="flex flex-cols justify-center items-center gap-2 mb-2">
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
		</div>

		

		<div>
			<button
				class="{buttonStyle} {blueStyle} w-full mr-2 mb-2"
				on:click={() => {
					pushPopup({
						status: 2, 
						message: 'This will not be an exact navigation.',
						onOk: () => {
								isOpen = false;
								_getNavigation();
						}
					});
				}
			}>
			Get Navigation
			</button>
			<button
				class="{buttonStyle} {blueStyle} w-full mr-2 mb-2"
				on:click={() => {
					pushPopup({
						status: 2, 
						message: 'This will be an exact navigation.',
						onOk: () => {
								isOpen = false;
								//_getAccurateNavigation();
								spendPointsHere(1750);
						}
					});
				}
			}>
			Get Exact Navigation
			</button>
		</div>

		<div class="flex ">
			<button
				class="{buttonStyle} {blueStyle} w-full mr-2"
				on:click={() => {
					pushPopup({
						status: 2,
						message: 'Are your sure you want to save these settings?',
						onOk: () => {
							isOpen = false;
							_updateSettings();
						}
					});
				}}
			>
				Save
			</button>
			<button
				class="{buttonStyle} {grayStyle} w-full"
				on:click={() => {
					isOpen = false;
				}}
			>
				Cancel
			</button>
		</div>

	</div>
</div>