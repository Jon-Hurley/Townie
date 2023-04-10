<script>
	import { onDestroy, onMount } from 'svelte';
	import { Game } from '../../../classes/Game';
	import { Location } from '../../../classes/Location';
    import { Map } from '../../../classes/Map';
    import { buttonStyle, redStyle } from '../../../css';
	import Timer from './timer.svelte';
    import { goto } from '$app/navigation';


    onMount(() => {
        Map.regenerate();
        Location.subscribe();
    });

    onDestroy(() => {
        Location.unsubscribe();
        Map.cancelSnapLocation();
    });

    const _skipLocation = async () => {
        popupOpen = false;
        //const skipped = await skipLocation();
        if (Game.player.destinationIndex === Game.destinations.length - 1) {
            
        }
        Game.player.destinationIndex++;
        Map.generateDestinationCircle();
        Map.setZoomAndCenter();
        //console.log("This works!");
    }

    let popupOpen = false;
    let tempText = Game.player.destinationIndex === Game.destinations.length - 1 ? "WARNING: This is the final destination! If you skip this, you will be sent to the game summary page!" : "Do you want to skip this destination? If you do, you will not gain points for this destination."
    
    const checkboxes = [
        {
            title: "Dark Mode",
            fn: () => Map.regenerate(),
            mapProp: "darkMode"
        },
        {
            title: "Snap Location",
            fn: () => Map.toggleSnapLocation(),
            mapProp: "snapLocation"
        }
    ]
</script>

<Timer/>

<div>
    <div>
        <button
		on:click={() => {
			popupOpen = true;
		}}
		name="skipLocationButton"
		id="skipLocation-btn"
		class="{buttonStyle} {redStyle} flex"
	>
		<div class="mr-2">Skip Location</div>
	</button>
    </div>
</div>

{#if popupOpen}
	<!--skipLocation popup-->
	<div
		class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
		id="skipLocation-popup"
	>
		<div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-md bg-white">
			<div class="mt-3 text-center">
				<div class="mx-auto flex items-center justify-center rounded-full">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-12 h-12 text-red-600"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<h3 class="text-lg leading-6 font-medium text-gray-900">Are you sure?</h3>
				<div class="px-7 py-3">
					<p class="text-sm text-gray-500">
						{tempText}
					</p>
				</div>

				<div class="mr-2 ml-2 grid grid-cols-2 gap-4 flex items-center px-4 py-3">
					<div>
						<button
							id="cancel-btn"
							on:click={() => {
								popupOpen = false;
							}}
							class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm hover:border-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
						>
							CANCEL
						</button>
					</div>
					<div>
						<button
							id="skip-btn"
							on:click={_skipLocation}
							class="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-red-400"
						>
							SKIP LOCATION
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
<!-- <div
    class="
        absolute top-[5rem] left-4 z-10
        bg-gray-800 rounded
        px-2 py-1
        opacity-50
    "
>
    {#each checkboxes as box}
        <div>
            <input
                id="checkbox"
                type="checkbox"
                class="
                    w-3 h-3
                    checked:bg-indigo-500
                    border:none
                    rounded
                    appearance-none
                    cursor-pointer
                    ring-2 ring-gray-400
                "
                bind:checked={Map[box.mapProp]}
                on:change={box.fn}
            >
            <label
                for="checkbox"
                class="ml-1 text-md text-gray-400"
            >
                {box.title}
            </label>
        </div>
    {/each}
</div> -->

<div
    class="full-screen"
    bind:this={Map.container}
/>

<style>
    .full-screen {
        width: 100vw;
        height: calc(100vh - 196px);
        margin: -16px;
		margin-bottom: 0px;
    }
</style>