<script>
	import { onMount } from 'svelte';
	import { inputStyle } from '../../../css';
    import { getUsers } from '../../../requests/search';
	import Username from '../../../general-components/username.svelte';

    let userSearch = '';
    let results = [];
    let suggestions = [];
    let displayResults = false;

    const updateResults = async() => {
        if (userSearch.length === 0) {
            results = suggestions;
            return;
        }
        results = await getUsers(userSearch);
        console.log(results)
    }

    onMount(async() => {
        suggestions = await getUsers('');
        results = suggestions;
    })

    let timeout = setTimeout(updateResults, 500);
</script>

<div
    class="
        w-full mb-4
        flex justify-end items-center
        focus:indigo-500
        text-gray-400
    "
>
    <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="w-6 h-6 absolute mr-2 w-10"
    >
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
    </svg>
    <input
        bind:value={userSearch}
        on:input={() => {
            clearTimeout(timeout);
            timeout = setTimeout(updateResults, 500);
        }}
        type="text"
        class="{inputStyle}"
        placeholder="Search Users"
        on:focusin={(e) => {
            e.stopPropagation();
            displayResults = true;
        }}
    >
</div>

{#if displayResults}
    <div class="absolute top-28 m-0 w-full left-0 p-4">
        <ul
            class="w-full rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
            tabindex="-1"
            role="listbox"
        >
            {#if !results?.length}
                <li class="p-2 text-gray-900 flex items-center">
                    <div class="w-1 h-8 mr-3 bg-gray-300 rounded-full"/>
                    <div>
                        No Results Found.
                    </div>
                </li>
                <hr class="h-[0.5px] bg-gray-100 mx-2">
            {:else}
                {#each results as r}
                    <li class="p-2">
                        <a
                            href={"/app/user/" + r.key}
                            class="flex justify-between items-center w-full"
                        >
                            <div class="flex items-center">
                                <div
                                    class="
                                        w-1 h-8 mr-3
                                        {
                                            r.isFriend ? 'bg-green-500'
                                            : r.jaccardIndex >= 0.25 ? 'bg-indigo-500'
                                            : 'bg-gray-300'
                                        }
                                        rounded-full
                                    "
                                />
                                <div class="text-gray-900 flex gap-2">
                                    <Username user={r}/>
                                    &bull;
                                    <div>
                                        {r.mutualFriends} Mutual Friend{r.mutualFriends !== 1 ? 's' : ''} 
                                    </div>
                                </div>
                            </div>
                            <div class="text-gray-300">
                                {r.jaccardIndex >= 0.25 && !r.isFriend ? 'Suggested' : ''}
                            </div>
                        </a>
                    </li>

                    <hr class="h-[0.5px] bg-gray-100 mx-2">
                {/each}
            {/if}

            <button
                class="flex justify-center text-gray-400 p-2 w-full"
                on:click={() => displayResults = false}
            >
                Hide Results
            </button>
        </ul>
    </div>
{/if}