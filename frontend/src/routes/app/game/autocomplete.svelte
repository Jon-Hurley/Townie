<script>
	import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';
    import { onMount } from "svelte";
    import { Geocoder } from "@beyonk/svelte-mapbox";

	import { Location } from "../../../classes/Location";
    
    export let settings;

    onMount(async() => {
        const res = await Location.getCurrentLocation();
        settings.lat = res.lat;
        settings.lon = res.lng;
    })
</script>

<Geocoder
    accessToken={PUBLIC_MAPBOX_TOKEN}
    options = {{
        proximity: {
            longitude: settings.lon,
            latitude: settings.lat
        }
    }}
    on:result={(e) => {
        console.log("LOC: ", e);
        settings.lat = e.detail.result.center[1];
        settings.lon = e.detail.result.center[0];
    }}
/>