<script>
	import { each } from 'svelte/internal';
import { blueStyle, buttonStyle, grayStyle, hr, largeTitle, inputStyle } from '../../../css';
	import { updateSettings } from '../../../requests/group';
    const section = "font-semibold text-lg text-center mb-3"

	export let settings;
    const form = { ...settings };
    let locationInput = "";
	let isOpen = true;

    $: () => {
        console.log(locationInput);
    };
    
    const _updateSettings = () => {
        updateSettings(form);
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
    ]
</script>

<button type="button" class="{buttonStyle} {grayStyle} w-full" on:click={() => (isOpen = true)}>
	Settings
</button>

<!--
    Background backdrop, show/hide based on modal state.

    Entering: "ease-out duration-300"
    From: "opacity-0"
    To: "opacity-100"
    Leaving: "ease-in duration-200"
    From: "opacity-100"
    To: "opacity-0"
-->

<!--
    Modal panel, show/hide based on modal state.

    Entering: "ease-out duration-300"
        From: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
        To: "opacity-100 translate-y-0 sm:scale-100"
    Leaving: "ease-in duration-200"
        From: "opacity-100 translate-y-0 sm:scale-100"
        To: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
-->

{#if isOpen}
	<div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
	<div
		class="
            fixed bottom-14 left-0
            w-screen text-center
        "
	>
		<div
            class="
                bg-gray-50 p-4 rounded-t-lg
                w-full
            "
        >
            <div class="{largeTitle}">
                Settings
            </div>
            <hr class="{hr} my-4">

            <div class="{section}">
                Starting Location
            </div>
			<input
                class="{inputStyle}"
                placeholder="Starting Location"
                bind:value={locationInput}
            />
            <hr class="{hr} my-4">
            
            <div class="{section}">
                Allowed Transport
            </div>
            <div
                class="flex justify-center gap-2"
                style="max-height: 100%"
            >
                {#each checkboxes as checkbox}
                    <button
                        class="{buttonStyle} {form[checkbox.field] ? blueStyle : grayStyle}"
                        on:click={() => {
                            form[checkbox.field] = !form[checkbox.field];
                            

                            for (let i = 0; i < checkboxes.length; i++) {
                                if (checkboxes[i] != checkbox) {
                                    form[checkboxes[i].field] = true
                                }
                            }
                        }}
                    >
                        {checkbox.title}
                    </button>
                {/each}
                
            </div>

            <hr class="{hr} my-4">
            <div
                class="
                    flex justify-between items-center
                    bg-white p-3 mb-2
                    border-2 border-gray-500 rounded
                "
            >
                <div class="font-semibold">
                    Theme
                </div>
                <select
                    bind:value={form.theme}
                    class="w-32"
                >
                    <option value="None">None</option>
                    <option value="Food">Food</option>
                    <option value="Choppa">Choppa</option>
                    <option value="Vroom">Vroom</option>
                </select>
            </div>
            <div
                class="
                    flex justify-between items-center
                    bg-white p-3 mb-2
                    border-2 border-gray-500 rounded
                "
            >
                <div class="font-semibold">
                    Length
                </div>
                <select
                    bind:value={form.desiredCompletionTime}
                    class="w-32"
                >
                    <option value={30}>30 minutes</option>
                    <option value={60}>60 minutes</option>
                    <option value={90}>90 minutes</option>
                    <option value={120}>120 minutes</option>
                    <option value={180}>180 minutes</option>
                </select>
            </div>
            <div
                class="
                    flex justify-between items-center
                    bg-white p-3
                    border-2 border-gray-500 rounded
                "
            >
                <div class="font-semibold">
                    Game Radius
                </div>
                <select
                    bind:value={form.radius}
                    class="w-32"
                >
                    <option value={1}>1 mile</option>
                    <option value={2}>2 miles</option>
                    <option value={5}>5 miles</option>
                    <option value={10}>10 miles</option>
                    <option value={20}>20 miles</option>
                </select>
            </div>
            

            <hr class="{hr} my-4">
			<div class="flex ">
				<button
					class="{buttonStyle} {blueStyle} w-full mr-2"
					on:click={() => {
						isOpen = false;
                        _updateSettings()
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
{/if}
