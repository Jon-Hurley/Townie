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
    class="container"
>
    <input
        bind:value={userSearch}
        on:input={() => {
            clearTimeout(timeout);
            timeout = setTimeout(getUsers, 500);
        }}
        type="text"
        class="w-full p-2 pl-8 rounded border border-gray-200 bg-gray-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-yellow-600 focus:border-transparent"
        placeholder="Search Users"
    >
    {#if userSearch.length}
        <ul
            class="absolute top-12 p-8 w-full z-10 mt-1 rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
            tabindex="-1"
            role="listbox"
            aria-labelledby="listbox-label"
            aria-activedescendant="listbox-option-3"
        >
            {#if results.length === 0}
                <li
                    class="w-full text-gray-900 relative cursor-default select-none py-2 pl-3 pr-9"
                >
                    No Results Found.
                </li>
            {:else}
                {#each results as r}
                    <li
                        class="w-full text-gray-900 relative cursor-pointer py-2 pl-3 pr-9"
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
    {/if}
</div>


<!-- <div class="">
    <div class="inline-flex flex-col justify-center relative text-gray-500">
        <div class="relative">
            <input type="text" class="p-2 pl-8 rounded border border-gray-200 bg-gray-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-yellow-600 focus:border-transparent" placeholder="search..." value="Gar" />
            <svg class="w-4 h-4 absolute left-2.5 top-3.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
        </div>
        <ul class="bg-white border border-gray-100 w-full mt-2">
            <li class="pl-8 pr-2 py-1 border-b-2 border-gray-100 relative cursor-pointer hover:bg-yellow-50 hover:text-gray-900">
                <svg class="absolute w-4 h-4 left-2 top-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <b>Gar</b>dameer - Italië
            </li>
            <li class="pl-8 pr-2 py-1 border-b-2 border-gray-100 relative cursor-pointer hover:bg-yellow-50 hover:text-gray-900">
                <svg class="absolute w-4 h-4 left-2 top-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <b>Gar</b>da - Veneto - Italië
            </li>
            <li class="pl-8 pr-2 py-1 border-b-2 border-gray-100 relative cursor-pointer hover:bg-yellow-50 hover:text-gray-900">
                <svg class="absolute w-4 h-4 left-2 top-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <b>Gar</b>da Hotel - Italië
            </li>
            <li class="pl-8 pr-2 py-1 border-gray-100 relative cursor-pointer hover:bg-yellow-50 hover:text-gray-900">
                <svg class="absolute w-4 h-4 left-2 top-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <b>Gar</b>dena Resort - Italië
            </li>
        </ul>
    </div>
</div> -->


<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 5px;
    }
</style>