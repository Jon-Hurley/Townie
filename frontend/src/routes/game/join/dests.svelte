<script>
	import { onMount } from "svelte";
	import { buttonStyle, indigoStyle } from "../../../css";
    import { gamePage } from "../../../stores";
    // temporary imports
    import { sendPreferences } from '../../../requests/gamesettings';
    import Loading from '../../../components/loading.svelte';

    let destinations = [];
    let loading = true;

//const updateResults = async() => {
//        const res = await sendPreferences();
//        console.log(res.data)
//        if (res) {
//            return res;
//        }
//        else {
//            return [];
//        }
//    }
    onMount(async() => {
        destinations = await sendPreferences();
        console.log(destinations.length)
        loading = false;
    });

</script>

{#if loading}
    <Loading/>
{:else}
    <div
            class="absolute top-28 m-0 w-full left-0 p-4"
        >
            <ul
                class="w-full rounded-md bg-white text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                tabindex="-1"
                role="listbox"
                aria-labelledby="listbox-label"
                aria-activedescendant="listbox-option-3"
            >
                {#if destinations.length === 0}
                    <li
                        class="
                            w-full z-10
                            bg-white
                            text-gray-900
                            relative
                            cursor-default
                            select-none
                            p-2
                        "
                    >
                        No Results Found.
                    </li>
                {:else}
                    {#each destinations as r}
                        <li
                            class="
                                w-full
                                text-gray-900
                                z-10
                                bg-white
                                relative
                                cursor-pointer
                                p-2
                                flex
                                justify-between
                            "
                        >
                        {r.name}
                        </li>
                    {/each}
                {/if}
            </ul>
        </div>
{/if}