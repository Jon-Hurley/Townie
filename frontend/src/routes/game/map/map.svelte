<script>
	import { onDestroy, onMount } from 'svelte';
	import { subscribeToLocation, unsubscribeToLocation, locationStore } from '../../../stores';
    import { PUBLIC_GOOGLE_MAPS_DARK_MODE, PUBLIC_GOOGLE_MAPS_LIGHT_MODE } from '$env/static/public';

	let container;
	let map;
    let darkMode = false;

    const createMap = () => {
        const mapLoc = map?.getCenter();
        map = new google.maps.Map(container, {
            zoom: 20,
            mapId: darkMode ? PUBLIC_GOOGLE_MAPS_DARK_MODE
                            : PUBLIC_GOOGLE_MAPS_LIGHT_MODE,
            disableDefaultUI: true
        });
        if (mapLoc) map.setCenter(mapLoc);
    }

    onMount(() => {
        createMap();
        subscribeToLocation(({ location }) => {
            if (!location) return;
            const center = new google.maps.LatLng(
                location.lat, location.lng
            );
            map.panTo(center);
        });
    })

    onDestroy(() => {
        unsubscribeToLocation();
    })
</script>

<div class="flex items-center absolute bottom-20 right-4 z-10">
    <input
        id="purple-checkbox"
        type="checkbox"
        class="w-4 h-4 text-indigo-600 bg-gray-100 border-gray-300 rounded focus:ring-indigo-500 dark:focus:ring-indigo-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
        bind:checked={darkMode}
        on:change={createMap}
    >
    <label for="purple-checkbox" class="ml-2 text-lg font-medium text-gray-400">
        Dark Mode
    </label>
</div>


<div
    class="full-screen"
    bind:this={container}
/>

<style>
    .full-screen {
        width: 100vw;
        height: calc(100vh - 120px);
        margin: -16px;
    }
</style>