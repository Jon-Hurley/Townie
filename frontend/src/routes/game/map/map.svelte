<script>
	import { onDestroy, onMount } from 'svelte';
	import { subscribeToLocation, unsubscribeToLocation, locationStore } from '../../../stores';
    import { PUBLIC_GOOGLE_MAPS_DARK_MODE, PUBLIC_GOOGLE_MAPS_LIGHT_MODE } from '$env/static/public';

	let mapState = {
        container: undefined,
        map: undefined,
        darkMode: false
    };

    const regenerateMap = () => {
        const mapLoc = mapState.map?.getCenter();
        mapState.map = new google.maps.Map(mapState.container, {
            zoom: 20,
            mapId: mapState.darkMode ? PUBLIC_GOOGLE_MAPS_DARK_MODE
                                     : PUBLIC_GOOGLE_MAPS_LIGHT_MODE,
            disableDefaultUI: true
        });
        if (mapLoc) mapState.map?.setCenter(mapLoc);
    }

    onMount(() => {
        regenerateMap();
        subscribeToLocation(mapState);
    });

    onDestroy(() => {
        unsubscribeToLocation();
    });

    const checkboxes = [
        {
            title: "Dark Mode",
            fn: regenerateMap,
            mapProp: "darkMode"
        },
        {
            title: "Snap Location",
            fn: () => {},
            mapProp: "snapLocation"
        }
    ]
</script>

<div
    class="
        absolute top-[5rem] left-4 z-10
        bg-gray-800 rounded
        px-3 py-1
    "
>
    {#each checkboxes as box}
        <div class="py-1">
            <input
                id="checkbox"
                type="checkbox"
                class="
                    w-4 h-4
                    checked:bg-indigo-500
                    border:none
                    rounded
                    appearance-none
                    cursor-pointer
                    ring-2 ring-gray-400
                "
                bind:checked={mapState[box.mapProp]}
                on:change={box.fn}
            >
            <label
                for="checkbox"
                class="ml-2 text-lg text-gray-400"
            >
                {box.title}
            </label>
        </div>
    {/each}
</div>


<div
    class="full-screen"
    bind:this={mapState.container}
/>

<style>
    .full-screen {
        width: 100vw;
        height: calc(100vh - 120px);
        margin: -16px;
    }
</style>