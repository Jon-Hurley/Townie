<script>
    import axios from 'axios';
    import { PUBLIC_BACKEND_API } from '$env/static/public'
    
    let userSearch = '';

    const getUsers = async() => {
        console.log("searching...", userSearch)

        try {
            const res = await axios.post(
                PUBLIC_BACKEND_API + 'user/search-users/',
                {
                    substr: userSearch
                }
            )
            console.log(res)
        } catch (e) {
            console.log(e)
        }
    }

    let timeout = setTimeout(getUsers, 500);
</script>

<div class="container">
    <input
        bind:value={userSearch}
        on:input={() => {
            clearTimeout(timeout);
            timeout = setTimeout(getUsers, 500);
        }}
        class="relative block w-full appearance-none rounded border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        placeholder="Search Users"
    >
</div>


<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 5px;
    }
</style>