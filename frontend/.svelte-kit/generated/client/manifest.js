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
	"/account/game_log": [6],
	"/account/password-reset": [7],
	"/account/verification": [8],
	"/game": [9,[2]],
	"/login": [10],
	"/notifs": [11],
	"/signup": [12],
	"/social": [13],
	"/store": [14],
	"/summary/[slug]": [15],
	"/user/[slug]": [16],
	"/verification": [17]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};