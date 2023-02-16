<script>
    import axios from 'axios';
    import { PUBLIC_BACKEND_API } from '$env/static/public'
    import { goto } from '$app/navigation'

    let displayResults = false;
    let userSearch = '';
    let results = [];

    const getUsers = async() => {
        console.log("searching...", userSearch)
        try {
            const res = await axios.post(
                PUBLIC_BACKEND_API + 'user/search-users/',
                { substr: userSearch }
            )
            if (res?.data?.users)
                results = res.data.users;
        } catch (e) {
            console.log(e)
        }
    }

    let timeout = setTimeout(getUsers, 500);
</script>



<div
    class="m-0 w-full p-2"
>
    <input
        bind:value={userSearch}
        on:input={() => {
            clearTimeout(timeout);
            timeout = setTimeout(getUsers, 500);
        }}
        type="text"
        class="m-0 w-full p-2 pl-8 rounded border border-gray-200 bg-gray-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-yellow-600 focus:border-transparent"
        placeholder="Search Users"
    >
</div>

{#if userSearch.length}
    <div
        class="absolute top-12 m-0 w-full p-2"
    >
        <ul
            class="w-full rounded-md bg-white text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
            tabindex="-1"
            role="listbox"
            aria-labelledby="listbox-label"
            aria-activedescendant="listbox-option-3"
        >
            {#if results.length === 0}
                <li
                    class="w-full text-gray-900 relative cursor-default select-none p-2"
                >
                    No Results Found.
                </li>
            {:else}
                {#each results as r}
                    <li
                        class="w-full text-gray-900 relative cursor-pointer p-2"
                        on:click={() => {
                            console.log("going")
                            goto('/user/' + r.id)
                        }}
                        on:keydown={() => {
                            console.log("going")
                            goto('/user/' + r.id)
                        }}
                    >
                        <!-- <img></img> -->
                        {r.username} #{r.id}
                    </li>
                {/each}
            {/if}
        </ul>
    </div>
{/if}