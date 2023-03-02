<script>
	import { onDestroy, onMount } from 'svelte';
	import { subscribeToLocation, unsubscribeToLocation, locationStore } from '../../../stores';
    import { PUBLIC_GOOGLE_MAPS_DARK_MODE, PUBLIC_GOOGLE_MAPS_LIGHT_MODE } from '$env/static/public';
    import { gameStore } from '../../../stores';
	import { get } from 'svelte/store';

	let mapState = {
        container: undefined,
        center: undefined,
        map: undefined,
        darkMode: false
    };

    // get(locationStore).index = 0;

    const randomizeLocation = (lat, lng, radius) => {
        var x0 = lng;
        var y0 = lat;
        var newRadius = radius / 100000;

        var randint = Math.random();
        var randint2 = Math.random();
        var scale = newRadius * Math.sqrt(randint);
        var scale2 = 2 * Math.PI * randint2;

        var xAdd = scale * Math.cos(scale2);
        var yAdd = scale * Math.sin(scale2);

        return {
            lat: yAdd + y0,
            lng: xAdd + x0
        }
    }

    const regenerateMap = (mapState) => {
        // let destinations = $gameStore.game.destinations;
        // let index = get(locationStore).index;
        // let currentDestination = currentDestination[0];
        // if (index != -1) {
        //     currentDestination = destinations[index];
        // } else {
        //     currentDestination = undefined;
        // }
        
        // if (index == destinations.length - 1) {
        //     get(locationStore).index = -1;
        // } else {
        //     get(locationStore).index = index + 1;
        // }
        


        mapState.map = new google.maps.Map(mapState.container, {
            zoom: 20,
            // TODO: Get user current location
            center: {lat: 40.4251, lng: -86.9129},
            mapId: mapState.darkMode ? PUBLIC_GOOGLE_MAPS_DARK_MODE
                                     : PUBLIC_GOOGLE_MAPS_LIGHT_MODE,
            disableDefaultUI: true
        });
        const mapLoc = mapState.map?.getCenter();
        const mapZoom = mapState.map?.getZoom();

        let circle = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map: mapState.map,
            //center: randomizeLocation({ lat: currentDestination.lat, lng: currentDestination.lng }),
            center: randomizeLocation(40.423538, -86.921738, 20),
            radius: 20,
        })

        let userCircle = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map: mapState.map,
            center: {lat: 40.4251, lng: -86.9129},
            radius: 20,
        })

        var bounds = new google.maps.LatLngBounds();
        bounds.extend(userCircle['center']);
        bounds.extend(circle['center']);
        mapState.map.setCenter(bounds.getCenter);
        mapState.map.fitBounds(bounds);

        const midpointLat = (userCircle['center']['lat'] + circle['center']['lat']) / 2;
        const midpointLng = (userCircle['center']['lng'] + circle['center']['lng']) / 2;
        mapState.map.setCenter({ lat: midpointLat, lng: midpointLng });

        
        if (mapLoc) mapState.map?.setCenter(mapLoc);
        if (mapZoom) mapState.map?.setZoom(mapZoom);
        mapState = mapState;
    }

    onMount(() => {
        const mapLoc = mapState.map?.getCenter();
        const mapZoom = mapState.map?.getZoom();
        mapState.map = new google.maps.Map(mapState.container, {
            zoom: 20,
            center: {lat: 40.4251, lng: -86.9129},
            mapId: mapState.darkMode ? PUBLIC_GOOGLE_MAPS_DARK_MODE
                                     : PUBLIC_GOOGLE_MAPS_LIGHT_MODE,
            disableDefaultUI: true
        });

        regenerateMap(mapState);
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