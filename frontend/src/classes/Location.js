import { writable, get } from 'svelte/store';
import { Map } from './Map';
import { Game } from './Game';

export class Location {
	static store = writable({ lat: null, lng: null });
    static interval = undefined;

    static getLocation() {
        return get(Location.store);
    }
    
    static async getCurrentLocation() {
        return await new Promise((res, rej) => {
            navigator.geolocation.getCurrentPosition(
                loc => res({
                    lat: loc.coords.latitude,
                    lng: loc.coords.longitude
                }),
                rej
            );
        });
    }

    static updateLocation(lat, lng) {
        Location.store.set({ lat, lng });
        if (Map.map) {
            Map.generateUserMarker({ lat, lng });
            Map.setZoomAndCenter();
        }
        Game.updateLocation(lat, lng);
    }

	static async subscribe() {
        if (Location.interval) return;
		Location.interval = navigator.geolocation.watchPosition(
            (loc) => {
                Location.updateLocation(
                    loc.coords.latitude,
                    loc.coords.longitude
                )
            },
            (err) => {
                console.log("Location error:", err);
                clearInterval(Location.interval);
                Location.interval = undefined;
            }
        );
	}

	static unsubscribe() {
		navigator.geolocation.clearWatch(Location.interval);
	}

    static randomize(lat, lng) {
        var x0 = lng;
        var y0 = lat;
        var newRadius = 20 / 100000;
        var randint = Math.random();
        var randint2 = Math.random();
        var scale = newRadius * Math.sqrt(randint);
        var scale2 = 2 * Math.PI * randint2;
        var xAdd = scale * Math.cos(scale2);
        var yAdd = scale * Math.sin(scale2);
        return { lat: yAdd + y0, lng: xAdd + x0 }
    };
};