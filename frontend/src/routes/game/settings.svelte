<script>
	import { onMount } from 'svelte';
    import { blueStyle, buttonStyle, grayStyle, hr, largeTitle, inputStyle } from '../../css';
	import { Game } from '../../classes/Game';
	import { getThemeList } from '../../requests/group';
	import Autocomplete from './autocomplete.svelte';
    const section = "font-semibold text-lg text-center mb-3";

    let form = {};
    
    onMount(() => {
        Game.store.subscribe(gs => {
            if (gs) {
                form = { ...gs.game.settings };
                form.otherCompletionTime = form.otherCompletionTime;
                form.otherRadius = form.otherRadius;
                form.otherBudget = form.otherBudget;
            }
        })
    })

    let otherCompletionTime = false;
    let otherRadius = false;
	let isOpen = true;
    let otherBudget = false;
    let randomThemeChosen = false;

    let themeValue = "";

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
    ]

    const _generateRandomTheme = async() => {
        let themes = await getThemeList();
        let realThemes = themes['themes']
        let index = Math.floor(2 * Math.random());
        let theme;
        if (realThemes[index] != undefined) {
            theme = realThemes[index]['theme'];
        } else {
            theme = "blank";
        }
        return theme;
    }
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
                on:change={async (e) => {
                    const v = e.target.value;
                    randomThemeChosen = v === "random";
                    if (!randomThemeChosen) {
                        console.log(v);
                        form.theme = v;
                        themeValue = v;
                    } else {
                        let v;
                        try {
                            v = await _generateRandomTheme();
                        } catch (err) {
                            console.log(err)
                            console.log("error with random theme generation")
                            v = "Restaurants"
                        }
                        switch (v) {
                            case 'Tourism':
                                v = 'tourist-attraction';
                                break;
                            case 'Restaurants':
                                v = 'restaurant';
                                break;
                            case 'Shopping':
                                v = 'store';
                                break;
                            case 'Museums':
                                v = 'museum';
                                break;
                            default:
                                v = 'no_theme';
                                break;
                        }
                        form.theme = v;
                        console.log(v);
                        themeValue = "random";
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
                on:input={e => {
                    let v;
                    try {
                        v = parseInt(e.target.value)
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
            bg-white p-3
            border-2 border-gray-200 rounded
        "
    >
        <div class="font-semibold">
            Max Budget Per Attraction
        </div>
        <select
            on:change={e => {
                const v = e.target.value;
                otherBudget = v === "Other";
                console.log("OtherBudget " + otherBudget)
                if (!otherBudget) {
                    form.budget = parseInt(v);
                    form = form;
                }
            }}
            value={form.budget}
            class="w-40"
        >
            <option value={0}>Free</option>
            <option value={1}>10 dollars</option>
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
                on:input={e => {
                    let v;
                    try {
                        v = parseInt(e.target.value)
                    } catch (err) {
                        v = 0;
                    }
                    const budget1 = Math.abs(v);
                    if (budget1 == 0) {
                        form.budget = 0;
                    }
                    else if (budget1 <= 10) {
                        form.budget = 1;
                    }
                    else if (budget1 <= 25) {
                        form.budget = 2;
                    }
                    else if (budget1 <= 50) {
                        form.budget = 3;
                    }
                    else if (budget1 > 50) {
                        form.budget = 4;
                    }
                }}
            />
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