<script>
	import { onMount } from 'svelte';
    import { blueStyle, buttonStyle, grayStyle, hr, largeTitle, inputStyle } from '../../../css';
	import { updateSettings } from '../../../requests/group';
	import { gameStore } from '../../../stores';
	import Autocomplete from './autocomplete.svelte';
    const section = "font-semibold text-lg text-center mb-3";

    let form = {};
    onMount(() => {
        gameStore.subscribe(gs => {
            if (gs) {
                form = { ...gs.game.settings };
                form.otherCompletionTime = form.otherCompletionTime;
            }
        })
    })

    let otherCompletionTime = false;
    let otherRadius = false;
	let isOpen = true;

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

{#if $gameStore}
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
        <div class="{largeTitle}">
            Settings
        </div>
        <hr class="{hr} my-4">

        <div class="{section}">
            Starting Location
        </div>
        <Autocomplete
            settings={form}
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
                    class="{buttonStyle} {form[checkbox.field] ? blueStyle : (grayStyle + ' opacity-25')}"
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

        <hr class="{hr} my-4">
        <div
            class="
                flex justify-between items-center
                bg-white p-3 mb-2
                border-2 border-gray-200 rounded
            "
        >
            <div class="font-semibold">
                Theme
            </div>
            <select
                bind:value={form.theme}
                class="w-40"
            >
                <option value="None">None</option>
                <option value="restaurant">Food</option>
                <option value="park">Park</option>
                <option value="museum">Museum</option>
            </select>
        </div>
        <div
            class="
                flex justify-between items-center
                bg-white p-3 mb-2
                border-2 border-gray-200 rounded
            "
        >
            <div class="font-semibold">
                Length
            </div>
            <select
                on:change={e => {
                    const v = e.target.value;
                    otherCompletionTime = v === "Other";
                    if (!otherCompletionTime) {
                        form.desiredCompletionTime = parseInt(v);
                    }
                }}
                value={form.desiredCompletionTime}
                class="w-40"
            >
                <option value={30}>30 minutes</option>
                <option value={60}>60 minutes</option>
                <option value={90}>90 minutes</option>
                <option value={120}>120 minutes</option>
                <option value={180}>180 minutes</option>
                <option value="Other">Other</option>
            </select>

            {#if otherCompletionTime}
                <input
                    class="w-40"
                    placeholder="Other"
                    type="number"
                    min="1"
                    value={form.desiredCompletionTime}
                    on:input={e => {
                        let v;
                        try {
                            v = parseInt(e.target.value)
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
                bg-white p-3
                border-2 border-gray-200 rounded
            "
        >
            <div class="font-semibold">
                Game Radius
            </div>
            <select
                on:change={e => {
                    const v = e.target.value;
                    otherRadius = v === "Other";
                    console.log("OtherRadius " + otherRadius)
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
                <option value={20}>20 miles</option>
                <option value={50}>50 miles</option>
                <option value={100}>Max: 100 miles</option>
                <option value="Other">Other</option>
            </select
>
            {#if otherRadius}
                <input
                    class="w-40"
                    placeholder="Other"
                    type="number"
                    min="1"
                    value={form.radius}
                    on:input={e => {
                        let v;
                        try {
                            v = parseInt(e.target.value)
                        } catch (err) {
                            v = 0;
                        }
                        form.radius = Math.abs(v);
                        if (form.radius > 100) {
                            form.radius = 100;
                        }
                    }}
                />
                <text>Nonnegative please :)</text>
            {/if}
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