<script>
    import { Map } from '../../../../classes/Map';
    const settingsStore = Map.settings;

    const checkboxes = [
        {
            title: "Dark Mode",
            fn: () => Map.toggleDarkMode(),
            mapProp: "darkMode"
        },
        {
            title: "Snap Location",
            fn: () => Map.toggleSnapLocation(),
            mapProp: "snapLocation"
        },
        {
            title: "Half Destination Radius",
            fn: () => { // EXAMPLE: shrink radius to 0 in 100 seconds
                const period = 100;
                const t = 100_000; // in 100 seconds, shrink radius to 0
                const rad = $settingsStore.destinationRadius;
                const reps = t / period;
                let i = 0;
                let interval = setInterval(() => {
                    Map.updateDestinationRadius(x => x - rad / reps);
                    if (i++ === reps) clearInterval(interval);
                }, period)
            },
            mapProp: "destinationRadius"
        },
        {
            title: "Double Destination Radius",
            fn: () => Map.updateDestinationRadius(x => 2 * x),
            mapProp: "destinationRadius"
        }
    ]
</script>

<div
    class="
        absolute top-[5rem] left-4 z-10
        bg-gray-800 rounded
        px-2 py-1
        opacity-50
    "
>
    {#each checkboxes as box}
        <div>
            <input
                id="checkbox"
                type="checkbox"
                class="
                    w-3 h-3
                    checked:bg-indigo-500
                    border:none
                    rounded
                    appearance-none
                    cursor-pointer
                    ring-2 ring-gray-400
                "
                bind:checked={Map.settings[box.mapProp]}
                on:change={box.fn}
            >
            <label
                for="checkbox"
                class="ml-1 text-md text-gray-400"
            >
                {box.title}
            </label>
        </div>
    {/each}
</div>