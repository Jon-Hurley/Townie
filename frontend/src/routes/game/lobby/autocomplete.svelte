<script>
	import { onMount } from "svelte";
	import { inputStyle } from "../../../css";
    
    export let settings;
    let input;

    onMount(async() => {
        const res = await new Promise((res, rej) => {
            navigator.geolocation.getCurrentPosition(res);
        });
        settings.lat = res.coords.latitude;
        settings.lon = res.coords.longitude;
        
        const autocomplete = new google.maps.places.Autocomplete(input);
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
            const lat = place.geometry.location.lat();
            const lon = place.geometry.location.lng();
            settings.lat = lat;
            settings.lon = lon;
        });
    })
</script>

<input
    type="text"
    id="autocomplete"
    size="50"
    bind:this={input}
    class="{inputStyle}"
/>