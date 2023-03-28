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
	() => import('./nodes/15')];

export const server_loads = [];

export const dictionary = {
	"/account": [3],
	"/account/edit": [4],
	"/account/password-reset": [5],
	"/account/verification": [6],
	"/game": [7,[2]],
	"/login": [8],
	"/notifs": [9],
	"/signup": [10],
	"/social": [11],
	"/store": [12],
	"/summary/[slug]": [13],
	"/user/[slug]": [14],
	"/verification": [15]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};