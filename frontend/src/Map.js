import {
    PUBLIC_GOOGLE_MAPS_DARK_MODE,
    PUBLIC_GOOGLE_MAPS_LIGHT_MODE
} from '$env/static/public';
import { userStore } from './stores';
import { get } from 'svelte/store';
import { Game } from './Game'
import { Location } from './Location';

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

        Map.generateUserMarker();
    	Map.generateDestinationCircle();
        Map.generatePlayerMarkers();

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

    static async generateUserMarker() {
        if (!Map.map) return;
        let latLng = await Location.getCurrentLocation()
        if (!latLng) return;
        if (Map.userLocation) {
            Map.userLocation.setMap(null);
        }
        // Change user's marker color
        console.log(latLng)
        Map.userLocation = new google.maps.Marker({
            position: { lat: latLng.coords.latitude, lng: latLng.coords.longitude },
            map: Map.map,
            //title: get(userStore).username
        });
    };

    static generateDestinationCircle() {
        const player = Game.getPlayer(get(userStore)?.username);
        if (!player) throw new Error("u don fuked up, no pp found :(");

        console.log(player);
        const tempDest = get(Game.store)?.destinations[player.destinationIndex];
        console.log(get(Game.store).destinations);
        const latLng = { lat: tempDest.latitude, lng: tempDest.longitude };

        if (!latLng) return;
        if (Map.nextDestination) {
            Map.nextDestination.setMap(null);
        }
        Map.nextDestination = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map: Map.map,
            center: Location.randomize(latLng.lat, latLng.lng),
            // center: randomizeLocation(40.423538, -86.921738, 20),
            radius: 20,
        })
    };

    static generatePlayerMarkers() {
        const players = get(Game.store)?.players;
        if (!players) return;
        if (Map.playerMarkerList) {
            for (let marker of Map.playerMarkerList) {
                marker?.setMap(null);
            }
        }
        Map.playerMarkerList = players.map((player) => {
            if (player._key === get(userStore).key) return;
            if (player.hidingState) {
                // Circle, hidden exact loc.
                // Go back and figure out names for circles
                return new google.maps.Circle({
                    strokeColor: "#FF0000",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: "#FF0000",
                    fillOpacity: 0.35,
                    map: Map.map,
                    center: Location.randomize(player.lat, player.lon),
                    radius: 20
                })
            } else {
                // Marker, shown exact loc.
                return new google.maps.Marker({
                    position: { lat: player.lat, lng: player.lon },
                    map: Map.map,
                    title: player.username
                })
            }
        })
    };
}