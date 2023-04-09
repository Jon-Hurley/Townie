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
    on:result={(loc) => {
        console.log(loc);
        settings.lat = loc.lat;
        settings.lon = loc.lng;
    }}
/>