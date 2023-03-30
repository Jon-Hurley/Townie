import { writable, get } from 'svelte/store';
import { Game } from './Game.js';

export class Location {
	static store = writable();
    static interval = undefined;

    static getLocation() {
        return get(Location.store);
    }
    
    static async getCurrentLocation() {
        return await new Promise((res, rej) => {
            navigator.geolocation.getCurrentPosition(res, rej);
        });
    }

    static updateLocation(loc) {
        const { latitude: lat, longitude: lng } = loc.coords;
        const oldLoc = Location.getLocation();
        console.log("Location interval...", {lat, lng});
        
        if (oldLoc && lat === oldLoc.lat && lng === oldLoc.lng) {
            return;
        }

        Location.store.set({ lat, lng });
        console.log('Location updated');
        Game.updateLocation(lng, lat);
    }

	static async subscribe() {
        if (Location.interval) return;

        const loc = await Location.getCurrentLocation();
        Location.updateLocation(loc);

		Location.interval = setInterval(() => {
            navigator.geolocation.getCurrentPosition(
                Location.updateLocation,
                (err) => {        
                    console.log("Location error:", err);
                    clearInterval(Location.interval);
                    Location.interval = undefined;
                }
            );
        }, 5000);       
	}

	static unsubscribe() {
		clearInterval(Location.interval);
	}
};