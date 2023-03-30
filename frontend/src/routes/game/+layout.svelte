<script>
    import { Game } from '../../classes/Game';
	import Loading from '../../general-components/loading.svelte';
    import Join from './join/join.svelte';
	import Lobby from './lobby/lobby.svelte';
	import Map from './map/map.svelte';
	import Subnav from './subnav.svelte';
	import AccountBar from '../account-bar.svelte';
	import Autocomplete from './lobby/autocomplete.svelte';
	import Tutorial from '../../general-components/tutorial.svelte';
    
    let gameStore = Game.store;
    let tutorialOpen;
    
    $: gamePage = $gameStore?.game?.page || 'join';
</script>

<div class="flex flex-col h-full">
    {#if gamePage === 'join'}
        <slot name="join">
            {#if tutorialOpen}
                <Tutorial/>
                <!-- Close Button -->
                <button class="absolute top-[5rem] right-4 md:right-40 lg:right-96 z-10
                    bg-red-100 rounded-full
                    opacity-80 text-red-600"
                    on:click={() => {
                        tutorialOpen = false;
                    }}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>               
                </button>
            {:else}
                <Join/>
                <button class="absolute top-[5rem] right-4 z-10
                    bg-gray-800 rounded-full
                    px-1 py-1
                    opacity-50 text-gray-400"
                    on:click={() => {
                        tutorialOpen = true;
                    }}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                    </svg>        
                </button> 
            {/if}
        </slot>
    {:else if gamePage === 'lobby'}
        <slot name="lobby">
            <Lobby/>
            <Subnav/>
        </slot>
    {:else if gamePage === 'map'}
        <slot name="map">
            <Map/>
            <Subnav/>
        </slot>
    {:else if gamePage === 'summary'}
        <slot name="summary">
        </slot>
    {/if}
</div>