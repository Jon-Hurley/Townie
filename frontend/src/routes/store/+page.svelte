<script>
    import Tutorial from "../../components/tutorial.svelte";

    $: hours = `00${Math.floor((elapsedTime/1000/60/60)%60)}`.slice(-2);
    $: minutes = `00${Math.floor((elapsedTime/1000/60)%60)}`.slice(-2);
    $: seconds = `00${Math.floor((elapsedTime/1000)%60)}`.slice(-2);
    $: formattedTime = `${hours}:${minutes}:${seconds}`;

    let startTime = 0;
    let elapsedTime = 0;
    let oldElapsedTime = 0;
    let interval;
    let state = 0; // 1 for running, 2 for paused

    const start = () => {
        startTime = Date.now();
        state = 1;
        interval = setInterval(() => {
            if (state === 1) {
                const endTime = Date.now();
                elapsedTime = endTime - startTime + oldElapsedTime;
            }
        });
        // AUTOPAUSE: IF AT A LOCATION
    }

    const pause = () => {
        state = 2; // 2 represents paused
        oldElapsedTime = elapsedTime;
    }

    const resume = () => {
        startTime = Date.now();
        state = 1; // 1 represents running
    }
</script>

<Tutorial/>

<!--
<button on:click={start}>
    Start
</button>
{#if state === 1}
    <button on:click={pause}>
        Pause
    </button>
{:else}
    <button on:click={resume}>
        Resume
    </button>
{/if}

<-- TIMER FEATURE ->
<div class="absolute top-[5rem] right-4 z-10
    bg-gray-800 rounded
    px-2 py-1
    opacity-50 text-gray-400">
    <h1 class="border-b border-gray-400">
        Total Time:
    </h1>
    {formattedTime}
</div> 
-->
