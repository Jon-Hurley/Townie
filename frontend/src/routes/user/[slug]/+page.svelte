<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getUser } from '../../../requests/search';
	import Loading from '../../../general-components/loading.svelte';
	import User from './user.svelte';

	let user;
	let rank;
	let level = 1;

	const loadUser = async () => {
		const key = $page.params.slug;
		console.log(key);
		user = await getUser(key);
		let points = user.cumPoints;
		level = await _pointsToLevel(points);
		await _getRank();
	};

	const _pointsToLevel = async (points) => {
		while (points >= 1000 && level < 5) {
			points -= 1000;
			level++;
		}

		if (points < 1000) {
			return level;
		}

		while (points >= 5000 && level < 15) {
			points -= 5000;
			level++;
		}

		if (points < 5000) {
			return level;
		}

		while (points >= 15000 && level < 25) {
			points -= 15000;
			level++;
		}

		if (points < 15000) {
			return level;
		}

		while (points >= level * 1000) {
			points -= level * 1000;
			level++;
		}

		return level;
	};

	// Set variable rank based on level
	// 1-4: Beginner
	// 5-14: Tourist
	// 15-24: Adventurer
	// 25-49: Traveler
	// 50-74: Citizen
	// 75-99: Resident
	// 100+: Townie
	const _getRank = () => {
		if (level < 5) {
			rank = 'Beginner';
		} else if (level < 15) {
			rank = 'Tourist';
		} else if (level < 25) {
			rank = 'Adventurer';
		} else if (level < 50) {
			rank = 'Traveler';
		} else if (level < 75) {
			rank = 'Citizen';
		} else if (level < 100) {
			rank = 'Resident';
		} else {
			rank = 'Townie';
		}
	};

	onMount(loadUser);
</script>

{#if user}
	<div class="h-full flex flex-col">
		<User {user} reloadUser={loadUser} {rank} />
	</div>
{:else}
	<Loading />
{/if}
