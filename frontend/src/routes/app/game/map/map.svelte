<script>
	import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';
    import { onDestroy, onMount } from 'svelte';
    import { Map as Mapbox, Marker } from '@beyonk/svelte-mapbox';
    import * as turf from '@turf/turf';

    import Timer from './timer.svelte';
    import Options from './options.svelte';

    import { Location } from '../../../../classes/Location';
    import { Map } from '../../../../classes/Map';
    import { Game } from '../../../../classes/Game';

    const gameStore = Game.store;
    const mapSettingsStore = Map.settings;
    const locationStore = Location.store;

    const onMapReady = async() => {
        const mapboxObj = Map.map.getMap();
        Map.setCenterToCurrent();
        Map.setDestinationCircle();
        // mapboxObj.setStyle('mapbox://styles/arnavmehra/cle7jp4jn003b01ntixmh28ea');
        gameStore.subscribe(Map.updateDestinationCircle);
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
</Mapbox>