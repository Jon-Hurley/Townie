<script>
	import { blueStyle, buttonStyle, grayStyle, hr, largeTitle } from '../../../../css';
	import { primaryColor } from '../../../../stores';
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
		console.log("skipping location");

		clearInterval(Game?.timerInterval);
		Game.timerInterval = null;
		
        if (Game.player.destinationIndex === Game.destinations.length - 1) {
            Game.leave();
            return;
        }

        incrementDestinationIndex(Game.player.connectionId);
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
            _shrinkRadius();
        } else if (pointsSpent == 1500) {
			isOpen = false;
            _getExactLocation();
        } else {
			_getAccurateNavigation();
		}
        
        return 0;
    }

	const _shrinkRadius = () => {
		Map.updateDestinationRadiusScalar(x => x * 0.5);
		console.log($settingsStore.destinationRadiusScalar);
        Map.setCenterToCurrent();
        Map.updateDestinationCircle();
        Map.updateBounds();
	}
	const _getExactLocation = () => {
		Map.updateDestinationRadiusScalar(x => 0);
        Map.setCenterToCurrent();
        Map.updateDestinationCircle();
        Map.updateBounds();
	}

</script>

<button type="button" class="{buttonStyle} {grayStyle} w-full" on:click={() => (isOpen = true)}>
	Options
</button>

<!--
<div
	class="
        fixed inset-0 bg-gray-200 mb-16
        pointer-events-none
        transition-all duration-500
        {isOpen ? 'bg-opacity-75' : 'bg-opacity-0'}
    "
/>
-->

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
					{#if $gameStore.game.settings.casual}
					<button
						on:click={() => {
							pushPopup({
								status: 2, 
								message: "Do you want to shrink the destination radius for the current destination?",
								onOk: () => {
										isOpen = false;
										_shrinkRadius();
								}
							});
						}}
						name="shrinkRadiusButton"
						id="shrinkRadius-btn"
						class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 flex z-500"
					>
						<div class="px-4">Shrink Radius</div>
					</button>
					{:else}
					<button
						on:click={() => {
							pushPopup({
								status: 2, 
								message: "Do you want to shrink the destination radius for 750 points?",
								onOk: () => {
										isOpen = false;
										let res = spendPointsHere(750);
								}
							});
						}}
						name="shrinkRadiusButton"
						id="shrinkRadius-btn"
						class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 flex z-500"
					>
						<div class="px-4">Shrink Radius</div>
					</button>
					{/if}
				</div>
			</div>
			
			<div>
				<div class="flex flex-cols justify-center items-center">
					{#if $gameStore.game.settings.casual}
						<button
							on:click={() => {
								pushPopup({
									status: 2,
									message: "Do you want to show the exact location of the current destination?",
									onOk: () => {
											isOpen = false;
											_getExactLocation();
									}
								});
							}}
							name="showExactButton"
							id="showExact-btn"
							class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 flex z-500"
						>
							<div class="px-4">Show Exact Location</div>
						</button>
					{:else}
						<button
							on:click={() => {
								pushPopup({
									status: 2, 
									message: "Do you want to show the exact location for 1500 points?",
									onOk: () => {
											isOpen = false;
											let res = spendPointsHere(1500);
									}
								});
							}}
							name="showExactButton"
							id="showExact-btn"
							class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 flex z-500"
						>
							<div class="px-4">Show Exact Location</div>
						</button>
					{/if}
				</div>
			</div>

			<div>
				<div class="flex flex-cols justify-center items-center">
					<button
						on:click={() => {
							pushPopup({
								status: 3, 
								message: 
									Game.player.destinationIndex === Game.destinations.length - 1
									? "WARNING: This is the final destination! If you skip this, you will be sent to the game summary page!"
									: Game.game.settings.casual
									? "Do you want to skip this destination?"
									: "Do you want to skip this destination? If you do, you will not gain points for this destination.",
								onOk: _skipLocation,
								includeCancel: true,
							});
						}}
						name="skipLocationButton"
						id="skipLocation-btn"
						class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 flex z-500"
					>
						<div class="px-4">Skip Location</div>
					</button>
				</div>
			</div>
		</div>

		

		<div>
			<button
				class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 w-full mr-2 mb-2"
				on:click={() => {
					pushPopup({
						status: 2, 
						message: 'Do you want to show navigation to the destination? This will not be an exact.',
						onOk: () => {
								isOpen = false;
								_getNavigation();
						}
					});
				}
			}>
			Get Navigation
			</button>
			{#if $gameStore.game.settings.casual}
				<button
					class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 w-full mr-2 mb-2"
					on:click={() => {
						pushPopup({
							status: 2, 
							message: 'Do you want to show the exact navigation to the current destination?',
							onOk: () => {
									isOpen = false;
									_getAccurateNavigation();
							}
						});
					}}>
					Get Exact Navigation
				</button>
			{:else}
				<button
					class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 w-full mr-2 mb-2"
					on:click={() => {
						pushPopup({
							status: 2, 
							message: 'Do you want to show the exact navigation to the destination for 1750 points?',
							onOk: () => {
									isOpen = false;
									//_getAccurateNavigation();
									spendPointsHere(1750);
							}
						});
					}}>
					Get Exact Navigation
				</button>
			{/if}
		</div>

		<div class="flex ">
			<button
				class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 w-full mr-2"
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