<script>
    import Tutorial from "../../components/tutorial.svelte";

    let locationMessage = true;

    $: lHours = `00${Math.floor((locationTime/1000/60/60)%60)}`.slice(-2);
    $: lMinutes = `00${Math.floor((locationTime/1000/60)%60)}`.slice(-2);
    $: lSeconds = `00${Math.floor((locationTime/1000)%60)}`.slice(-2);
    $: formattedLocationTime = `${lHours}:${lMinutes}:${lSeconds}`;

    $: gHours = `00${Math.floor((gameTime/1000/60/60)%60)}`.slice(-2);
    $: gMinutes = `00${Math.floor((gameTime/1000/60)%60)}`.slice(-2);
    $: gSeconds = `00${Math.floor((gameTime/1000)%60)}`.slice(-2);
    $: formattedGameTime = `${gHours}:${gMinutes}:${gSeconds}`;

    let startTime = 0;
    let locationTime = 0;
    let gameTime = 0;
    let oldGameTime = 0;
    let oldLocationTime = 0;
    let interval;
    let state = 1; // 1 for Game, 2 for Location
    let gameTimer = true;


    const startGame = () => {
        startTime = Date.now();
        state = 1;
        
        interval = setInterval(() => {
            if (state === 1) {
                const endTime = Date.now();
                gameTime = endTime - startTime + oldGameTime;
            } if (state === 2) {
                const endTime = Date.now();
                locationTime = endTime - startTime;
            }
        });
    }


    const pause = () => {
        if (state === 1) {
            startTime = Date.now();
        }
        state = 2; // 2 represents paused
        gameTimer = false;
        oldGameTime = gameTime;
    }

    const resume = () => {
        startTime = Date.now();
        state = 1; // 1 represents running
        gameTimer = true;
    }
</script>

<!--<Tutorial/>-->


<button on:click={startGame}>
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

<!-- TIMER FEATURE -->
{#if gameTimer}
    <button class="absolute top-[5rem] right-4 z-10
        bg-gray-800 rounded
        px-2 py-1
        opacity-50 text-gray-400"
        on:click={pause}>
        <h1 class="border-b border-gray-400">
            Total Time:
        </h1>
        {formattedGameTime}
    </button> 
{:else}
    <button class="absolute top-[5rem] right-4 z-10
        bg-gray-800 rounded
        px-2 py-1
        opacity-50 text-gray-400"
        on:click={(() => gameTimer = true)}>
        <h1 class="border-b border-gray-400">
            Location Time:
        </h1>
        {formattedLocationTime}
    </button> 
{/if}

{#if !locationMessage}
    <!--Location popup-->
    <div class="z-50 fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="location-popup">
        <div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
            <div class="mt-3 text-center">
                <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 01-.982-3.172M9.497 14.25a7.454 7.454 0 00.981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 007.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 002.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 012.916.52 6.003 6.003 0 01-5.395 4.972m0 0a6.726 6.726 0 01-2.749 1.35m0 0a6.772 6.772 0 01-3.044 0" />
                      </svg>                                      
                </div>

                <h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">
                    Congrats!
                </h3>
                <div class="px-7">
                    <p class="text-sm text-gray-500">
                        Your have reached your destination! The game timer has been paused and will resume once you leave your location.
                    </p>
                </div>
        
                <div class="mr-2 ml-2 flex items-center px-4 py-3">
                    <button 
                        id="ok-btn"
                        on:click={() => {
                            locationMessage = null;
                        }}
                        class="px-4 py-2 border border-green-600 text-green-600 text-base font-medium rounded-md w-full shadow-sm bg-green-100 hover:border-green-800 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400"
                    >
                        OK
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}