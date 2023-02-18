<script>
    import axios from 'axios';
    import { PUBLIC_BACKEND_API } from '$env/static/public'
    import { goto } from '$app/navigation'

    let userSearch = '';
    let results = [];

    const getUsers = async() => {
        if (userSearch.length === 0) {
            results = [];
            return;
        }
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


<div class="w-full flex justify-end items-center relative focus:indigo-500 text-gray-400">
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
            timeout = setTimeout(getUsers, 500);
        }}
        type="text"
        class="m-0 w-full p-2 pl-8 rounded border border-gray-200 bg-gray-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
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
            aria-labelledby="listbox-label"
            aria-activedescendant="listbox-option-3"
        >
            {#if results.length === 0}
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
                {#each results as r}
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
                        <a href={"/user/" + r.id}>
                            <!-- <img></img> -->
                            {r.username} #{r.id}
                        </a>
                    </li>
                {/each}
            {/if}
        </ul>
    </div>
{/if}