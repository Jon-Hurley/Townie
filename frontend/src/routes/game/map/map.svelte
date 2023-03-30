<script>
	import { onDestroy, onMount } from 'svelte';
	import { Location }  from '../../../classes/Location'
    import { Map } from '../../../classes/Map'

	import Newtime from './newtime.svelte';

    onMount(async() => {
        await Map.regenerate();
        await Location.subscribe();
    });

    onDestroy(() => {
        Location.unsubscribe();
        Map.cancelSnapLocation();
    });
    
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

<div
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
</div>

<div
    class="full-screen"
    bind:this={Map.container}
/>

<div>
    <Newtime/>
</div>
<style>
    .full-screen {
        width: 100vw;
        height: calc(100vh - 120px);
        margin: -16px;
    }
</style>