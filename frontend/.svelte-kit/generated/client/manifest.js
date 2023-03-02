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
	() => import('./nodes/13'),
	() => import('./nodes/14'),
	() => import('./nodes/15'),
	() => import('./nodes/16')];

export const server_loads = [];

export const dictionary = {
	"/": [2],
	"/account": [3],
	"/account/edit": [4],
	"/forgot-password": [5],
	"/game": [6],
	"/game/lobby": [7],
	"/game/map": [8],
	"/login": [9],
	"/notifs": [10],
	"/password-reset": [11],
	"/signup": [12],
	"/social": [13],
	"/store": [14],
	"/user/[slug]": [15],
	"/verification": [16]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};