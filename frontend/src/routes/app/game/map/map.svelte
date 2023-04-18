<script>
	import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';
    import { onDestroy, onMount } from 'svelte';
    import { Map as Mapbox, Marker } from '@beyonk/svelte-mapbox';
    import { userStore, pushPopup } from '../../../../stores';
    import { buttonStyle, blueStyle } from '../../../../css';
    import * as turf from '@turf/turf';
    import { get } from 'svelte/store';

    import Timer from './timer.svelte';
    import Options from './options.svelte';

    import { Location } from '../../../../classes/Location';
    import { Map } from '../../../../classes/Map';
    import { Game } from '../../../../classes/Game';

    const gameStore = Game.store;
    const mapSettingsStore = Map.settings;
    const locationStore = Location.store;

    const title = 'text-gray-700 font-semibold text-lg mt-4';
    //let showDestination = false;

    let skipPopupOpen = false;
    let shrinkPopupOpen = false;
    let exactLocationPopupOpen = false;
    let errorPopupOpen = false;

    let tempText = (Game.player.destinationIndex === Game.destinations.length - 1) ? "WARNING: This is the final destination! If you skip this, you will be sent to the game summary page!" : "Do you want to skip this destination? If you do, you will not gain points for this destination."; 

    const onMapReady = async() => {
        const mapboxObj = Map.map.getMap();
        Map.setCenterToCurrent();
        Map.setDestinationCircle();
        // mapboxObj.setStyle('mapbox://styles/arnavmehra/cle7jp4jn003b01ntixmh28ea');
        gameStore.subscribe(() => {
            if (Map.map) {
                Map.updateDestinationCircle();
            }
        });
        locationStore.subscribe(Map.updateBounds);
    }

    onMount(() => {
        Location.subscribe();
    });

    onDestroy(() => {
        Location.unsubscribe();
        // Map.cancelSnapLocation();
    });

</script>

<Timer/>

<Options/>

<Mapbox
    accessToken={PUBLIC_MAPBOX_TOKEN}
    bind:this={Map.map}
    on:ready={onMapReady}
    zoom={$mapSettingsStore.zoom}
>
    {#each $gameStore.players as player}
        {#if player.username !== $gameStore.player.username
             && player.lat !== null && player.lon !== null}
            <Marker
                lng={player.lon}
                lat={player.lat}
                color="rgb(255,0,0)"
            />
        {/if}
    {/each}

    

    <Marker
        lng={$locationStore.lng}
        lat={$locationStore.lat}
        label={'You'}
        color="rgb(255,0,0)"
    />

    {#if $mapSettingsStore.destinationRadius * $mapSettingsStore.destinationRadiusScalar < .1}
        
        <Marker
            lng={Game.nextDestination.lon}
            lat={Game.nextDestination.lat}
            label={'Next Destination'}
            color="rgb(0,255,0)"
        />
    {/if}

    
</Mapbox>