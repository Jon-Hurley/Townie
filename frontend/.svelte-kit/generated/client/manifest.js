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
	() => import('./nodes/14')];

export const server_loads = [];

export const dictionary = {
	"/": [2],
	"/account": [3],
	"/game": [4],
	"/game/lobby": [5],
	"/game/map": [6],
	"/login": [7],
	"/login/new password": [8],
	"/notifs": [9],
	"/signup": [10],
	"/signup/verification": [11],
	"/social": [12],
	"/store": [13],
	"/user/[slug]": [14]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};