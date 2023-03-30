import {
    PUBLIC_GOOGLE_MAPS_DARK_MODE,
    PUBLIC_GOOGLE_MAPS_LIGHT_MODE
} from '$env/static/public';
import { Location } from './Location';
import { Game } from './Game';
import { get } from 'svelte/store';
import { userStore } from '../stores';

export class Map {
    static container = undefined;
    static map = undefined;
    static darkMode = false;
    static snapLocation = false;
    static snapInterval = undefined;

    static playerMarkerList = undefined;
    static nextDestination = undefined;
    static userMarker = undefined;
    static bounds = undefined;

    static async regenerate() {
        const mapLoc = Map.map?.getCenter();
        const mapZoom = Map.map?.getZoom();
        const loc = await Location.getCurrentLocation();
        
        Map.map = new google.maps.Map(Map.container, {
            zoom: 20,
            center: loc,
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

    static setZoomAndCenter() {
        Map.bounds = new google.maps.LatLngBounds();

        for (let player of Game.players) {
            Map.bounds.extend({ lat: player.lat, lng: player.lon });
        }
        if (Map.nextDestination) {
            Map.bounds.extend(Map.nextDestination.getCenter());
        }
        
        Map.map.fitBounds(Map.bounds);
        Map.map.setCenter(Map.bounds.getCenter());
    }

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
        if (!Game.player) return;

        if (Map.userMarker) {
            Map.userMarker.setMap(null);
        }
        Map.userMarker = new google.maps.Marker({
            position: { lat: Game.player.lat, lng: Game.player.lon },
            map: Map.map,
            // icon: {
            //     path: "M79.428,323.02l0.902,0.722l400,259.455c6.787,5.189,13.406,7.714,20.202,7.714c8.269,0,16.004-3.996,20.695-10.688 c5.548-7.923,6.236-17.791,2.041-29.33l-0.958-2.638l-166.234-247.27c-0.863-4.152-0.851-10.389,0.027-14.547L522.182,42.785 l0.979-2.653c4.254-11.545,3.599-21.433-1.952-29.392C516.521,4.015,508.764,0,500.462,0c-6.744,0-13.326,2.484-20.089,7.585 L81.487,262.942l-1.873,1.334c-9.293,7.356-14.645,18.045-14.679,29.324C64.899,304.883,70.184,315.602,79.428,323.02z M432.659,92.635l-118.072,173.22l-0.979,2.656c-5.354,14.535-5.4,35.652-0.107,50.208l0.958,2.635l118.67,176.517 L118.461,293.769L432.659,92.635z",
            //     fillColor: "#6366f1",
            //     fillOpacity: 1,
            //     rotation: 0,
            //     scale: 2,
            //     strokeWeight: 1,
            //     anchor: new google.maps.Point(10, 10)
            // },
            title: 'You'
        });
    };

    static generateDestinationCircle() {
        if (!Game.nextDestination) return;
        if (!Map.map) return;

        const latLng = {
            lat: Game.nextDestination.lat,
            lng: Game.nextDestination.lon
        };

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
            radius: 50,
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
            if (player.key === get(userStore).key) return;
            if (player.hidingState) {
                const latLng = Location.randomize(player.lat, player.lon);
                // Circle, hidden exact loc.
                // Go back and figure out names for circles
                return new google.maps.Circle({
                    strokeColor: "#FF0000",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: "#FF0000",
                    fillOpacity: 0.35,
                    map: Map.map,
                    center: latLng,
                    radius: 20
                })
            } else {
                const latLng = { lat: player.lat, lng: player.lon };
                // Marker, shown exact loc.
                return new google.maps.Marker({
                    position: latLng,
                    map: Map.map,
                    title: player.username
                })
            }
        })
    };
}