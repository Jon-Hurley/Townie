<script>
	import { inputStyle } from '../../../css';
    import { getUsers } from '../../../requests/search';

    let userSearch = '';
    let results = [];

    const updateResults = async() => {
        results = await getUsers(userSearch);
        console.log(results)
    }

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
    >
</div>

{#if userSearch.length}
    <div
        class="absolute top-28 m-0 w-full left-0 p-4"
    >
        <ul
            class="w-full rounded-md bg-white text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
            tabindex="-1"
            role="listbox"
        >
            {#if results.length === 0}
                <li class="p-2">
                    No Results Found.
                </li>
            {:else}
                {#each results as r, i}
                    <li class="p-2">
                        <a
                            href={"/app/user/" + r.key}
                            class="flex justify-between items-center w-full"
                        >
                            <div class="flex items-center">
                                <div
                                    class="
                                        w-1 h-6 mr-3
                                        {
                                            r.isFriend ? 'bg-green-500'
                                            : r.suggestion ? 'bg-indigo-500'
                                            : 'bg-gray-300'
                                        }
                                        rounded-full
                                    "
                                />
                                <div>
                                    {r.username} #{r.key}
                                </div>
                            </div>
                            {#if r.suggestion}
                                <div class="text-gray-300">
                                    Suggested
                                </div>
                            {/if}                
                        </a>
                    </li>
                    
                    {#if i !== results.length - 1}
                        <hr class="h-[1px] bg-gray-100 mx-2">
                    {/if}
                {/each}
            {/if}
        </ul>
    </div>
{/if}