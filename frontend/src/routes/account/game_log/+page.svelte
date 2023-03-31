<script>
	import { onMount } from 'svelte';
	//import AccountBar from "../../../components/account-bar.svelte";
	import Loading from '../../../general-components/loading.svelte';
	import { goto } from '$app/navigation';
	import {
		buttonStyle,
		gridItem,
		indigoStyle,
		redStyle,
		greenStyle,
		largeTitle,
		listItem,
		grayStyle
	} from '../../../css';
	import { getGameLog } from '../../../requests/search';
	import { rating } from '../../../requests/search';
	import { each, get_root_for_style } from 'svelte/internal';
	const title = 'text-gray-700 font-semibold text-lg mt-2';
	const hr = 'bg-gray-100 h-[2px] mt-4';

	let loading = true;
	let gameLog = [];
	let themes = [];

	onMount(async () => {
		gameLog = await getGameLog();
		console.log(gameLog[0].game.settings.theme);
		for (let i = 0; i < gameLog.length; i++) {
			themes[i] = await rating(gameLog[i].game.settings.theme);
		}
		console.log(gameLog);
		console.log(themes);
		loading = false;
	});

	function getTime(totalSeconds) {
		totalSeconds = Math.floor(totalSeconds / 1000);
		let hours = Math.floor(totalSeconds / 3600);
		totalSeconds %= 3600;
		let minutes = Math.floor(totalSeconds / 60);
		let seconds = totalSeconds % 60;
		let tmpHour = hours == 1 ? 'hour' : 'hours';
		let tmpMinute = minutes == 1 ? 'minute' : 'minutes';
		let tmpSecond = seconds == 1 ? 'second' : 'seconds';
		return `${hours} ${tmpHour} : ${minutes} ${tmpMinute} : ${seconds} ${tmpSecond}`;
	}
</script>

{#if loading}
	<Loading />
{:else if gameLog.length}
	<div class="flex flex-col h-full">
		<div class={largeTitle}>
			Previous Games:
			<div class="{title} text-center">
				{gameLog.length} Game(s) Played
			</div>
		</div>

		<hr class={hr} />
		<div class="rounded h-full overflow-auto p-2">
			<div
				class="
                    overflow-auto
                    inline-flex flex-wrap justify-center
                    gap-2
                    p-2
                    w-full
                "
				style="max-height: 100%"
			>
				{#each gameLog as log, i}
					<button
						class="{log.player.finished ? greenStyle : redStyle}
                                border-2
                                {log.player.finished ? 'border-green-600' : 'border-red-600'}
                                p-2
                                rounded
                                {log.player.finished ? 'bg-green-100/50' : 'bg-red-100/50'}         
                    "
						on:click={() => goto('/summary/' + log.game._key)}
					>
						<div class="{buttonStyle}{indigoStyle}" style="padding:2px;">
							{getTime(log.player.totalTime)}
						</div>
						<div>
							Points Gained: {log.player.points}
						</div>
						<div>
							Number of Destinations Completed: {log.player.destinationIndex + 1}
						</div>
						<div>
							Theme: {log.game.settings.theme} (Rating: {themes[i].rating} / 5)
						</div>
					</button>
				{/each}
			</div>
		</div>
		<hr class={hr} />
	</div>
{:else}
	<div class="flex flex-col h-full">
		<div class={largeTitle}>
			Previous Games:
			<div class="{title} text-center">You have no games played.</div>
		</div>
	</div>
{/if}
