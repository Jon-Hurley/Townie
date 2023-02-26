<script>
	import { onDestroy, onMount } from 'svelte';
	import { subscribeToLocation, unsubscribeToLocation, locationStore } from '../../../stores';
    import { PUBLIC_GOOGLE_MAPS_DARK_MODE, PUBLIC_GOOGLE_MAPS_LIGHT_MODE } from '$env/static/public';

	let mapState = {
        container: undefined,
        map: undefined,
        darkMode: false
    };

    let location=locationStore;

    const regenerateMap = () => {
        const mapLoc = mapState.map?.getCenter();
        const mapZoom = mapState.map?.getZoom();
        mapState.map = new google.maps.Map(mapState.container, {
            zoom: 20,
            mapId: mapState.darkMode ? PUBLIC_GOOGLE_MAPS_DARK_MODE
                                     : PUBLIC_GOOGLE_MAPS_LIGHT_MODE,
            disableDefaultUI: true
        });

        let circle = new google.maps.Circle({
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: "#FF0000",
        fillOpacity: 0.35,
        map: mapState.map,
        center: { lat: 40.423538, lng: -86.921738 },
        radius: 20,
    })
        if (mapLoc) mapState.map?.setCenter(mapLoc);
        if (mapZoom) mapState.map?.setZoom(mapZoom);
        mapState = mapState;
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
                bind:checked={mapState[box.mapProp]}
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