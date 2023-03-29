<script>
	import { onMount } from "svelte";
	//import AccountBar from "../../../components/account-bar.svelte";
	import Loading from "../../../components/loading.svelte";
    import { buttonStyle, gridItem, indigoStyle, redStyle, greenStyle, largeTitle, listItem } from "../../../css";
	import { getGameLog } from "../../../requests/search";
    const title = "text-gray-700 font-semibold text-lg mt-2";
    const hr = "bg-gray-100 h-[2px] mt-4"; 
    
    let loading = true;
    let gameLog = [];
    
    onMount(async () => {
        gameLog = await getGameLog();
        loading = false;
    });
</script>

{#if loading}
    <Loading/>
{:else if gameLog.length}
    <div class="flex flex-col h-full">
        <div class="{largeTitle}">
            Previous Games:
            <div class="{title} text-center">
                {gameLog.length} Game(s) Played
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
                {#each gameLog as game}
                    <div class="{game['destinationsCompleted'] == game['totalDestinations'] ? greenStyle : redStyle}
                                border-2
                                {game['destinationsCompleted'] == game['totalDestinations'] ? "border-green-600" : "border-red-600"}
                                p-2
                                rounded
                                {game['destinationsCompleted'] == game['totalDestinations'] ? "bg-green-100/50" : "bg-red-100/50"}         
                    ">
                        <div>
                            Time Spent Playing: {game['timeSpent']}
                        </div>
                        <div>
                            Points Gained: {game['points']}
                        </div>
                        <div>
                            Number of Destinations Completed: {game['destinationsCompleted']} / {game['totalDestinations']}
                        </div>
                    </div>
                {/each}
            </div>
        </div>
        <hr class={hr}>
    </div>
{:else}
    <div class="flex flex-col h-full">
        <div class="{largeTitle}">
            Previous Games:
            <div class="{title} text-center">
                You have no games played.
            </div>
        </div>
        
    </div>
{/if}