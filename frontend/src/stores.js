import { writable } from 'svelte/store';

export const userStore = writable();

export const mapStore = writable();

export const gamePage = writable('/game/join');