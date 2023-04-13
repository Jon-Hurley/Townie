<script>
	import { onMount } from 'svelte';
	import { Game } from '../../../../classes/Game';
	import { pushPopup } from '../../../../stores';

	let timeStore = Game.timeStore;
	$: paused = $timeStore;
    $: console.log({paused})
	$: if (paused) {
		lockedOntoTotalTimer = false;
		showPausedTime = true;
	} else {
		lockedOntoTotalTimer = true;
		showPausedTime = false;
	}

	let prev;
	$: {
		if (prev !== paused) {
			if (prev === true && paused === false) {
				pushPopup({
					status: 0,
					message: 'You have left the current destination. Your total time will resume counting.'
				});
			}
			prev = paused;
		}
	}

	onMount(() => {
		prev = null;
	})

    let interval;
    let lockedOntoTotalTimer;
	let locationTime = 0;
	let totalTime = 0;
	let showPausedTime = false;

	$: lHours = `00${Math.floor((locationTime / 60 / 60) % 60)}`.slice(-2);
	$: lMinutes = `00${Math.floor((locationTime / 60) % 60)}`.slice(-2);
	$: lSeconds = `00${Math.floor((locationTime) % 60)}`.slice(-2);
	$: formattedPausedTime = `${lHours}:${lMinutes}:${lSeconds}`;

	$: gHours = `00${Math.floor((totalTime / 60 / 60) % 60)}`.slice(-2);
	$: gMinutes = `00${Math.floor((totalTime / 60) % 60)}`.slice(-2);
	$: gSeconds = `00${Math.floor((totalTime) % 60)}`.slice(-2);
	$: formattedTotalTime = `${gHours}:${gMinutes}:${gSeconds}`;

	onMount(() => {
		interval = setInterval(() => {
			if (paused) {
				locationTime++;
			} else {
				totalTime++;
			}
		}, 1000);
	});

	//start location timer and pause game timer
	const toggle = () => {
        if (!lockedOntoTotalTimer) {
            showPausedTime = !showPausedTime;
        }
	}; 
</script>

<button
	class="absolute top-[5rem] right-4 z-10
    bg-gray-800 rounded
    px-2 py-1
    opacity-60 text-gray-400"
	on:click={toggle}
>
	<h1 class="border-b border-gray-400">
		{showPausedTime ? 'Location' : 'Total'} Time:
	</h1>
	{showPausedTime ? formattedPausedTime : formattedTotalTime}
</button>
