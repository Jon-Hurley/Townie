import { writable, get } from 'svelte/store';
import { Location } from './Location';
import { Game } from './Game';
import * as turf from '@turf/turf';
import { shrinkFactor, showDestination } from "../routes/app/game/map/map.svelte";

export class Map {
    static map = undefined;
    static settings = writable({
        darkMode: true,
        snapLocation: false,
        zoom: 15,
        destinationRadius: 1
    })
    static snapInterval = undefined;

    static toggleSnapLocation() {}
    static toggleDarkMode() {}

    static async setCenterToCurrent() {
        if (!Location.lat) {
            const loc = await Location.getCurrentLocation();
            Map.setCenter(loc);
        } else {
            Map.setCenter(Location.getLocation());
        }
    };

    static updateDestinationRadius(f) {
        Map.settings.update(settings => {
            settings.destinationRadius = f(settings.destinationRadius);
            return settings;
        });
        Map.updateDestinationCircle();
    }

    static setCenter(loc) {
        if (!loc || !loc.lat || !loc.lng || !Map.map) return;
        Map.map.flyTo({
            center: [ loc.lng, loc.lat ]
        });
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

    static getDestinationCircle() {
        const nextDest = Game.nextDestination;
        const center = [ nextDest.lon, nextDest.lat ];
        const radius = get(Map.settings).destinationRadius;
        const options = { steps: 50, units: 'kilometers' };
        return turf.circle(center, radius, options);
    }

    static setDestinationCircle() {
        const circle = Map.getDestinationCircle();
        const mapboxObj = Map.map.getMap();
        console.log(mapboxObj);
        
        mapboxObj.addSource("destCircleData", {
            "type": "geojson",
            "data": circle
        });
        mapboxObj.addLayer({
            id: "destCircle",
            type: "fill",
            source: "destCircleData",
            paint: {
                "fill-color": "red",
                "fill-opacity": 0.25,
            }
        });
    }

    static updateDestinationCircle() {
        const circle = Map.getDestinationCircle();
        const mapboxObj = Map.map.getMap();
        const src = mapboxObj.getSource("destCircleData");
        src?.setData(circle);
    }

    static updateBounds() {
        // Map.setCenterToCurrent();
        const mapboxObj = Map.map.getMap();
        console.log(Map.map, mapboxObj);
        
        const features = [
            turf.point([ Location.lng, Location.lat ])
        ]
        
        const nextDest = Game.nextDestination;
        console.log(nextDest);
        if (nextDest) {
            features.push(turf.point([ nextDest.lon, nextDest.lat ]));
        }

        for (let player of Game.players) {
            if (player.username !== Game.player.username
                && player.lat !== null && player.lon !== null) {
                features.push(turf.point([ player.lon, player.lat ]));
            }
        }

        const bbox = turf.bbox({
            type: 'FeatureCollection',
            features
        });
        console.log({bbox, features});
        Map.map.fitBounds(bbox);
    }
}