<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	import Loading from '../../../general-components/loading.svelte';

	import { buttonStyle, redStyle, greenStyle, largeTitle, hr } from '../../../css';
	import { primaryColor } from '../../../stores';
	import { getGameLog } from '../../../requests/search';
	import { userStore } from '../../../stores';

	const title = 'text-gray-700 font-semibold text-lg mt-2';

	let loading = false;
	let gameLog = [];

	const _getGameLog = async () => {
		loading = true;
		gameLog = await getGameLog($userStore.key);
		loading = false;
	}

	onMount(_getGameLog);

	const getTime = (totalMilliseconds) => {
		const date = new Date(null);
		const totalSeconds = Math.floor(totalMilliseconds / 1000);
		date.setSeconds(totalSeconds);
		return date.toISOString().slice(11, 19);
	}

	const themeMap = {
		'tourist_attraction': 'Tourism',
		'restaurant': 'Food',
		'store': 'Shopping',
		'museum': 'Museums'
	}
</script>

{#if loading}
	<Loading />
{:else if gameLog.length}
	<div class="flex flex-col h-full">
		<div class={largeTitle}>
			Previous Games
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
						class="
							{log.player.numCompleted == log.dests.length ? greenStyle : redStyle}
							{log.player.numCompleted == log.dests.length ? 'border-green-600' : 'border-red-600'}
							{log.player.numCompleted == log.dests.length ? 'bg-green-100/50' : 'bg-red-100/50'}         
							rounded border-2 p-2 flex justify-between w-56
						"
						on:click={() => goto('/app/game-summary/' + log.game._key)}
					>
						<div class="flex flex-col items-start">
							<div class="text-{$primaryColor}-500 border-{$primaryColor}-500">Points Gained</div>
							<div>Elapsed Time</div>
							<div>Dest Completed</div>
							<div>Theme</div>
						</div>
						<div class="flex flex-col items-end">
							<div class="text-{$primaryColor}-500 border-{$primaryColor}-500">{log.player.points}</div>
							<div>{getTime(log.player.totalTime)}</div>
							<div>{log.player.numCompleted} / {log.dests.length}</div>
							<div>{themeMap[log.game.settings.theme]}</div>
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
			Previous Games
			<div class="{title} text-center">
				You have no games played.
			</div>
		</div>
	</div>
{/if}