<script>
	import { onMount } from "svelte/types/runtime/internal/lifecycle";
    import { buttonStyle, gridItem, indigoStyle, redStyle, greenStyle, largeTitle, listItem } from "../../../css";
    import { Loading } from '../../components/loading.svelte';

    const title = "text-gray-700 font-semibold text-lg mt-2";
    const hr = "bg-gray-100 h-[2px] mt-4"; 
    
    let loading = true;
</script>

{#if loading}
    <Loading/>
{:else if $gameLogStore}
<div class="flex flex-col h-full">
    <div class="{largeTitle}">
        Previous Games:
        <div class="{title} text-center">
            {$gameLogStore.games.length} Game(s) Played
        </div>
    </div>

    <hr class={hr}>
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
            {#each $gameLogStore.games as game}
                {#if game['destinationsCompleted'] == game['totalDestinations']}
                    <div class="{gridItem} {greenStyle}">
                        Time Spent Playing: {game['timeSpent']}
                        Points Gained: {game['points']}
                        Number of Destinations Completed: {game['totalDestinations']} / {game['totalDestinations']}
                    </div>
                {:else}
                    <div class="{gridItem} {redStyle}">
                        Time Spent Playing: {game['timeSpent']}
                        Points Gained: {game['points']}
                        Number of Destinations Completed: {game['destinationsCompleted']} / {game['totalDestinations']}
                    </div>
                {/if}
            {/each}
            <div class="{gridItem}">
                <button>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
    <hr class={hr}>
</div>
{:else}
    <div class="{listItem}">
        You have no games played.
    </div>
{/if}