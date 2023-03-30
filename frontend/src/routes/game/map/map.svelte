<script>
	import { onDestroy, onMount } from 'svelte';
	import { subscribeToLocation, unsubscribeToLocation, locationStore } from '../../../stores';
    import { PUBLIC_GOOGLE_MAPS_DARK_MODE, PUBLIC_GOOGLE_MAPS_LIGHT_MODE } from '$env/static/public';
    import { gameStore } from '../../../stores';
	import { get } from 'svelte/store';
	import { each } from 'svelte/internal';

    $: hours = `00${((elapsedTime/1000/60/60)%60)}`.slice(-2);
    $: minutes = `00${((elapsedTime/1000/60)%60)}`.slice(-2);
    $: seconds = `00${((elapsedTime/1000)%60)}`.slice(-2);
    $: formattedTime = `${hours}:${minutes}:${seconds}`;

    let startTime = 0;
    let elapsedTime = 0;
    let oldElapsedTime = 0;
    let interval;
    let state = 0; // 1 for running, 2 for paused

    const start = () => {
        startTime = Date.now();
        state = 1;
        interval = setInterval(() => {
            if (state === 1) {
                const endTime = Date.now();
                elapsedTime = endTime - startTime + oldElapsedTime;
            }
        });
        // AUTOPAUSE: IF AT A LOCATION
    }

    const pause = () => {
        state = 2; // 2 represents paused
        oldElapsedTime = elapsedTime;
    }

    const resume = () => {
        startTime = Date.now();
        state = 1; // 1 represents running
    }

	let mapState = {
        container: undefined,
        center: undefined,
        map: undefined,
        darkMode: false
    };

    let markerList = [];
    let circleList = [];

    locationStore.set({
        ...location,
        index: 0
    })

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

        return { lat: yAdd + y0, lng: xAdd + x0 }
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

        let currentIndex = $locationStore.index;
        locationStore.set({
            ...locationStore,
            index: currentIndex + 1
        })

        console.log($gameStore);

        //let currentDestination = getDestWithIndex(currentIndex, $gameStore.destinations);
        let currentDestination = $gameStore.destinations[currentIndex];
        


        mapState.map = new google.maps.Map(mapState.container, {
            zoom: 20,
            // TODO: Get user current location
            center: { lat: 38.2400, lng: -85.6994},
            mapId: mapState.darkMode ? PUBLIC_GOOGLE_MAPS_DARK_MODE
                                     : PUBLIC_GOOGLE_MAPS_LIGHT_MODE,
            disableDefaultUI: true
        });
        const mapLoc = mapState.map?.getCenter();
        const mapZoom = mapState.map?.getZoom();

        //console.log(randomizeLocation(currentDestination.latitude, currentDestination.longitude, 20));
        
        let alteredCoords = randomizeLocation(currentDestination.latitude, currentDestination.longitude, 20);

        console.log(alteredCoords)
        let circle = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map: mapState.map,
            center: alteredCoords,
            // center: randomizeLocation(40.423538, -86.921738, 20),
            radius: 20,
        })

        console.log(circle.center.lat())

        let userCircle = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map: mapState.map,
            center: { lat: 38.2400, lng: -85.6994},
            radius: 20,
        })

        var bounds = new google.maps.LatLngBounds();

        for (let i = 0; i < gameStore.players.length; i++) {
            if (gameStore.players[i]['showLocation']) {
                let marker = new google.maps.Marker({
                    position: { lat: gameStore.players[i]['lat'], lng: gameStore.players[i]['lon'] },
                    map: mapState.map,
                    title: gameStore.players[i]['username']
                });
                markerList.push(marker);
                bounds.extend(marker['position']);
            } else {
                let circle = new google.maps.Circle({
                    strokeColor: "#FF0000",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: "#FF0000",
                    fillOpacity: 0.35,
                    map: mapState.map,
                    center: { lat: gameStore.players[i]['lat'], lng: gameStore.players[i]['lng'] },
                    radius: 20
                });
                markerList.push(circle);
                bounds.extend(circle['center']);
            }
        }

        // bounds.extend(userCircle['center']);
        // bounds.extend(circle['center']);
        mapState.map.setCenter(bounds.getCenter());
        mapState.map.fitBounds(bounds);

        const midpointLat = (userCircle['center']['lat']() + circle['center']['lat']()) / 2;
        const midpointLng = (userCircle['center']['lng']() + circle['center']['lng']()) / 2;

        console.log({ lat: midpointLat, lng: midpointLng })
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
        start();
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

    const getDestWithIndex = (index, destinations) => {
        for (let i = 0; i < destinations.length; i++) {
            if (destinations[i]['index'] == index) {
                return destinations[i];
            }
        }

        return undefined;
    }
</script>

<!-- TIMER FEATURE -->
<div class="absolute top-[5rem] right-4 z-10
    bg-gray-800 rounded
    px-2 py-1
    opacity-50 text-gray-400">
    <h1 class="border-b border-gray-400">
        Total Time:
    </h1>
    {formattedTime}
</div> 

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
