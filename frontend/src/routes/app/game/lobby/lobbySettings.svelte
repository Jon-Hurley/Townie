<script>
	import { blueStyle, buttonStyle, grayStyle, hr, largeTitle } from '../../../../css';
	import { primaryColor } from '../../../../stores';
	import { Game } from '../../../../classes/Game';
	import { getThemeList } from '../../../../requests/search';
	import Autocomplete from '../autocomplete.svelte';
	const section = 'font-semibold text-lg text-center mb-3';
	console.log($primaryColor)

    let gameStore = Game.store;
	let form = {
        ...$gameStore.game.settings
    };

	let isOpen = false;
	
	let otherCompletionTime = false;
	let otherRadius = false;
	let otherBudget = false;
	let randomThemeChosen = false;

	let themeValue = 'restaurant';

	const _updateSettings = () => {
		Game.updateSettings(form);
	};

	const checkboxes = [
		{
			field: 'walkingAllowed',
			title: 'Walk'
		},
		{
			field: 'drivingAllowed',
			title: 'Car'
		},
		{
			field: 'bicyclingAllowed',
			title: 'Bike'
		},
		{
			field: 'transitAllowed',
			title: 'Public Transportation'
		}
	];

	const _generateRandomTheme = async () => {
		let themes = await getThemeList();
		let realThemes = themes['themes'];
		for (let i = 0; i < realThemes.length; i++) {
			console.log("Theme " + i + ": " + realThemes[i]['theme'] + "")
		}
		let index = Math.floor(3 * Math.random());
		let theme;
		if (realThemes[index] != undefined) {
			theme = realThemes[index]['theme'];
		} else {
			theme = 'blank';
		}
		console.log(theme);
		return theme;
	};
</script>

<button type="button" class="{buttonStyle} {grayStyle} w-full" on:click={() => (isOpen = true)}>
	Settings
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
		<div class={largeTitle}>Settings</div>
		<hr class="{hr}"/>

		<div class={section}>Starting Location</div>
		<Autocomplete settings={form} />
		<hr class="{hr}"/>

		<div class={section}>Allowed Transport</div>
		<div class="flex justify-center gap-2" style="max-height: 100%">
			{#each checkboxes as checkbox}
				<button
					class="{buttonStyle} {form[checkbox.field] ? 
					'text-' + $primaryColor + '-500 border-' + $primaryColor +'-500 bg-white' 
					: grayStyle + ' opacity-25'}"
					on:click={() => {
						for (const { field } of checkboxes) {
							form[field] = false;
						}
						form[checkbox.field] = true;
					}}
				>
					{checkbox.title}
				</button>
			{/each}
		</div>

		<hr class="{hr}"/>
		<div
			class="
                flex justify-between items-center
                bg-white p-3 mb-2
                border-2 border-gray-200 rounded
            "
		>
			<div class="font-semibold">Theme</div>
			<select
				on:change={async (e) => {
					const v = e.target.value;
					randomThemeChosen = v === 'random';
					if (!randomThemeChosen) {
						console.log(v);
						form.theme = v;
						themeValue = v;
					} else {
						let v;
						try {
							v = await _generateRandomTheme();
						} catch (err) {
							console.log(err);
							console.log('error with random theme generation');
							v = 'restaurant';
						}
                        // const themeMap = {
                        //     'Tourism': 'tourist-attraction',
                        //     'Restaurants': 'restaurant',
                        //     'Shopping': 'store',
                        //     'Museums': 'museum'
                        // }
						form.theme = v || 'no_theme';
						themeValue = 'random';
					}
				}}
				value={themeValue}
				class="w-40"
			>
				<option value="tourist_attraction">Tourism</option>
				<option value="restaurant">Food</option>
				<option value="store">Shopping</option>
				<option value="museum">Museum</option>
				<option value="random">Random</option>
			</select>
		</div>

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

		<div
			class="
                flex justify-between items-center
                bg-white p-3 mb-2
                border-2 border-gray-200 rounded
            "
		>
			<div class="font-semibold">Game Radius</div>
			<select
				on:change={(e) => {
					const v = e.target.value;
					otherRadius = v === 'Other';
					console.log('OtherRadius ' + otherRadius);
					if (!otherRadius) {
						form.radius = parseInt(v);
						form = form;
					}
				}}
				value={form.radius}
				class="w-40"
			>
				<option value={1}>Min: 1 mile</option>
				<option value={2}>2 miles</option>
				<option value={5}>5 miles</option>
				<option value={10}>10 miles</option>
				<option value={15}>15 miles</option>
				<option value={20}>20 miles</option>
				<option value={25}>Max: 25 miles</option>
				<option value="Other">Other</option>
			</select>

			{#if otherRadius}
				<input
					class="w-40"
					placeholder="Other"
					type="number"
					min="1"
					value={form.radius}
					on:input={(e) => {
						let v;
						try {
							v = parseInt(e.target.value);
						} catch (err) {
							v = 0;
						}
						form.radius = Math.abs(v);
						if (form.radius > 25) {
							form.radius = 25;
						}
					}}
				/>
			{/if}
		</div>
		<div
			class="
            flex justify-between items-center
            bg-white p-3 mb-2
            border-2 border-gray-200 rounded
        "
		>
			<div class="font-semibold">Max Attraction Budget</div>
			<select
				on:change={(e) => {
					const v = e.target.value;
					otherBudget = v === 'Other';
					console.log('OtherBudget ' + otherBudget);
					if (!otherBudget) {
						form.budget = parseInt(v);
						form = form;
					}
				}}
				value={form.budget}
				class="w-40"
			>
				<option value={1}>Most affordable</option>
				<option value={2}>25 dollars</option>
				<option value={3}>50 dollars</option>
				<option value={4}>Splurge!</option>
				<option value="Other">Other</option>
			</select>

			{#if otherBudget}
				<input
					class="w-40"
					placeholder="Other"
					type="number"
					min="0"
					value={form.budget}
					on:input={(e) => {
						let v;
						try {
							v = parseInt(e.target.value);
						} catch (err) {
							v = 0;
						}
						const budget1 = Math.abs(v);
						if (budget1 == 0) {
							form.budget = 1;
						} else if (budget1 <= 10) {
							form.budget = 1;
						} else if (budget1 <= 25) {
							form.budget = 2;
						} else if (budget1 <= 50) {
							form.budget = 3;
						} else {
							form.budget = 4;
						}
					}}
				/>
			{/if}
		</div>

		<div
			class="
                flex justify-between items-center
                bg-white p-3
                border-2 border-gray-200 rounded
            "
		>
		<div class="font-semibold">Casual Mode</div>
			<input 
				type="checkbox" 
				value = "form.casual"
				bind:checked={form.casual}
				class="w-4 h-4 border border-gray-300 rounded focus:ring-3 focus:ring-{$primaryColor}-600 accent-{$primaryColor}-600"/>
		</div>

		<hr class="{hr} my-4" />
		<div class="flex ">
			<button
				class="{buttonStyle} text-{$primaryColor}-500 border-{$primaryColor}-500 w-full mr-2"
				on:click={() => {
					isOpen = false;
					_updateSettings();
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
