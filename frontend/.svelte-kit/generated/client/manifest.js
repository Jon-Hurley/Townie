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
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13')];

export const server_loads = [];

export const dictionary = {
	"/": [3],
	"/account": [4],
	"/game": [5,[2]],
	"/game/join": [6,[2]],
	"/game/lobby": [7,[2]],
	"/game/map": [8,[2]],
	"/login": [9],
	"/notifs": [10],
	"/social": [11],
	"/store": [12],
	"/user/[slug]": [13]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};