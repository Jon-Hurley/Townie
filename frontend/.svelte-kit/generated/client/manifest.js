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
	"/": [2],
	"/account": [3],
	"/game": [4],
	"/game/lobby": [5],
	"/game/map": [6],
	"/login": [7],
	"/notifs": [8],
	"/signup": [9],
	"/social": [10],
	"/store": [11],
	"/user/[slug]": [12],
	"/verification": [13]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};