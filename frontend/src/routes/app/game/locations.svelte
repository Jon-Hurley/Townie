<script>
	import { Game } from "../../../classes/Game";
	import { blueStyle, buttonStyle, grayStyle, hr, largeTitle } from "../../../css";
    import { primaryColor } from "../../../stores";
    const section = "font-semibold text-lg text-center mb-3";
    let isOpen = false;
    let gameStore = Game.store;
    $: destinations = (
        $gameStore?.destinations || []
    );
</script>
<button
    type="button"
    class="{buttonStyle} {blueStyle}"
    on:click={() => isOpen = true}
>
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
    <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
</svg>
  
</button>
<div
    class="
        fixed inset-0 bg-gray-200 mb-16
        pointer-events-none
        transition-all duration-500
        {isOpen ? 'bg-opacity-75' : 'bg-opacity-0'}
    "
/>
<div
    class="
        fixed left-0 bottom-16
        w-screen text-left
        transition-all duration-500
        {isOpen ? 'translate-y-0' : 'translate-y-full pointer-events-none'}
    "
>
    <div
        class="
            bg-gray-50 p-4 rounded-t-lg
            w-full 
        "
    >
        <div class="{largeTitle}">
            Location Itinerary
        </div>
        <hr class="{hr} my-4">
        
        <div class="text-lg p-2 mx-14 min-h-[50vh]">
            {#each destinations as destination, i}
                <div class="flex justify-between py-2 border-b border-gray-300">
                    <div>
                        <span class="font-bold mr-4">
                            #{i + 1}
                        </span>
                        <span>
                            {destination.name}
                        </span>
                    </div>
                </div>
            {/each}
        </div>
        
        <hr class="{hr} my-4" />
		<div class="flex ">
			<button
				class="{buttonStyle} {grayStyle} w-full"
				on:click={() => {
					isOpen = false;
				}}
			>
				Cancel
			</button>
		</div>
    </div>
</div>