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
	() => import('./nodes/16'),
	() => import('./nodes/17')];

export const server_loads = [];

export const dictionary = {
	"/": [3],
	"/account": [4],
	"/account/edit": [5],
	"/account/password-reset": [6],
	"/account/verification": [7],
	"/game": [8,[2]],
	"/game/join": [9,[2]],
	"/game/lobby": [10,[2]],
	"/game/map": [11,[2]],
	"/login": [12],
	"/notifs": [13],
	"/signup": [14],
	"/social": [15],
	"/store": [16],
	"/user/[slug]": [17]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};