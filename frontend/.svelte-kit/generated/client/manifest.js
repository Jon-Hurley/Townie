export { matchers } from './matchers.js';

export const nodes = [() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9')];

export const server_loads = [];

export const dictionary = {
	"/": [2],
	"/account": [3],
	"/game/lobby": [4],
	"/game/map": [5],
	"/login": [6],
	"/notifs": [7],
	"/social": [8],
	"/store": [9]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};