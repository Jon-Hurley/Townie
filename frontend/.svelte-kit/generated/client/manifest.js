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
	"/": [3],
	"/account": [4],
	"/account/edit": [5],
	"/account/password-reset": [6],
	"/account/verification": [7],
	"/game": [8,[2]],
	"/login": [9],
	"/notifs": [10],
	"/signup": [11],
	"/social": [12],
	"/store": [13],
	"/summary/[slug]": [14],
	"/user/[slug]": [15],
	"/verification": [16]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};