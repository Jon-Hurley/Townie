<script>
	import { blueStyle, buttonStyle, grayStyle, hr, largeTitle } from '../../../css';
	import { Game } from '../../../classes/Game';
	import { pushPopup } from '../../../stores';

    let gameStore = Game.store;
	let form = {
        ...$gameStore.game.settings
    };

	let otherCompletionTime = false;
	let isOpen = false;

	const _updateSettings = () => {
		Game.updateTime(form);
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
	</div>
</div>