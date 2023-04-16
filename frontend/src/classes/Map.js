import { writable, get } from 'svelte/store';
import { Location } from './Location';
import { Game } from './Game';
import * as turf from '@turf/turf';

export class Map {
    static map = undefined;
    static settings = writable({
        darkMode: true,
        snapLocation: false,
        zoom: 15,
        destinationRadius: 1,
        destinationRadiusScalar: 1,
        exactLocation: false
    })
    static snapInterval = undefined;

    static shrinkFactor = 1.0;

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
            if (settings.destinationRadius < 0.1) settings.destinationRadius = 0;
            return settings;
        });
        Map.updateDestinationCircle();
    }
    
    static updateDestinationRadiusScalar(f) {
        Map.settings.update(settings => {
            console.log("radius before: " + settings.destinationRadiusScalar);
            settings.destinationRadiusScalar = f(settings.destinationRadiusScalar);
            console.log("radius after: " + settings.destinationRadiusScalar);
            return settings;
        });
        Map.updateDestinationCircle();
    }

    static updateExactLocation(f) {
        console.log("before " + Map.settings.exactLocation);
        console.log(f(Map.settings.exactLocation))
        Map.settings.update(settings => {
            Map.settings.exactLocation = f(Map.settings.exactLocation);
            return settings;
        });
        console.log("after " + Map.settings.exactLocation);
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
        const settings = get(Map.settings);
        const nextDest = Game.nextDestination;
        const center = [ nextDest.lon, nextDest.lat ];
        const radius = settings.destinationRadius;
        const options = { steps: 50, units: 'kilometers' };
        return turf.circle(center, radius, options);
    }

    static getDestinationMarker() {
        const nextDest = Game.nextDestination;
        const center = [ nextDest.lon, nextDest.lat ];
        return turf.point(center);
    }

    static setDestinationCircle() {
        const circle = Map.getDestinationCircle();
        const mapboxObj = Map.map.getMap();
        console.log(mapboxObj);
        
        mapboxObj.addSource("destData", {
            "type": "geojson",
            "data": circle
        });
        mapboxObj.addLayer({
            id: "destCircle",
            type: "fill",
            source: "destData",
            paint: {
                "fill-color": "red",
                "fill-opacity": 0.25,
            }
        });
    }

    static updateDestinationCircle() {
        console.log("UpdateCircle: exactLocation: " + Map.settings.exactLocation);
        if (get(Map.settings).destinationRadius < 0.1 || Map.settings.exactLocation) {
            console.log("Radius is: " + get(Map.settings).destinationRadius)
            const point = Map.getDestinationMarker();
            const mapboxObj = Map.map.getMap();
            const src = mapboxObj.getSource("destData");
            src?.setData(point);
        } else {
            const circle = Map.getDestinationCircle();
            const mapboxObj = Map.map.getMap();
            const src = mapboxObj.getSource("destData");
            src?.setData(circle);
        }
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