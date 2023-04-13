<script>
	import { blueStyle, buttonStyle, grayStyle, hr, largeTitle } from '../../../../css';
	import { Game } from '../../../../classes/Game';
	import { Map } from '../../../../classes/Map';
	import { Location } from '../../../../classes/Location'; 
	import { pushPopup } from '../../../../stores';
	import { get } from 'svelte/store';
	import * as turf from '@turf/turf';

	const settingsStore = Map.settings;

    let gameStore = Game.store;
	let form = {
        ...$gameStore.game.settings
    };

	let otherCompletionTime = false;
	let isOpen = false;

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
		let finalLat;
		if (addLat > 0.5) {
			finalLat = currLat + randPos;
			console.log(finalLat);
		} else {
			finalLat = currLat - randPos;
			console.log(finalLat);
		}
		
		exportNav = finalLat + "," + destLng;
		url = "https://www.google.com/maps/dir/?api=1&dir_action=navigate&destination=" + exportNav;
		window.open(url, "_blank");
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
            w-full
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
		<div class="flex ">
			<button
				class="{buttonStyle} {blueStyle} w-full mr-2"
				on:click={() => {
					pushPopup(
						2, 'Are your sure you want to save these settings?',
						() => {
							isOpen = false;
							_updateSettings();
						}
					);
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
		<div>
			<button
				class="{buttonStyle} {blueStyle} w-full mr-2"
				on:click={() => {
					pushPopup(
						2, 'Are you sure you want to navigate? It will only be the rough area.',
						() => {
							isOpen = false;
							_getNavigation();
						}
					)
				}
			}>
			Get navigation
			</button>
		</div>
	</div>
</div>