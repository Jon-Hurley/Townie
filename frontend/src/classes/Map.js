import {
    PUBLIC_GOOGLE_MAPS_DARK_MODE,
    PUBLIC_GOOGLE_MAPS_LIGHT_MODE
} from '$env/static/public';
import { Location } from './classes/Location';

export class Map {
    static container = undefined;
    static map = undefined;
    static darkMode = false;
    static snapLocation = false;
    static snapInterval = undefined;

    static async regenerate() {
        const mapLoc = Map.map?.getCenter();
        const mapZoom = Map.map?.getZoom();
        const loc = await Location.getCurrentLocation();
        console.log({loc})
        Map.map = new google.maps.Map(Map.container, {
            zoom: 20,
            center: { lat: 40.4251, lng: -86.9129 },
            mapId: Map.darkMode ? PUBLIC_GOOGLE_MAPS_DARK_MODE
                                 : PUBLIC_GOOGLE_MAPS_LIGHT_MODE,
            disableDefaultUI: true
        });
        if (mapLoc && mapZoom) {
            Map.map.setCenter(mapLoc);
            Map.map.setZoom(mapZoom);
        }
    };

    static setCenter(loc) {
        if (!loc || !loc.lat || !loc.lng) return;
        const center = new google.maps.LatLng(loc.lat, loc.lng);
        Map.map.panTo(center);
    };

    static toggleSnapLocation() {
        if (Map.snapLocation) {
            Map.snapInterval = setInterval(() => {
                Map.setCenter(Location.getLocation());
            }, 1000);
        } else {
            Map.cancelSnapLocation();
        }
    };

    static cancelSnapLocation() {
        if (!Map.snapInterval) return;
        Map.snapLocation = false;
        clearInterval(Map.snapInterval);
        Map.snapInterval = undefined;
    };
}