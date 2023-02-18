<script>
    import axios from 'axios';
    import { PUBLIC_BACKEND_API } from '$env/static/public';
	import { onMount } from 'svelte';
    import { userStore } from '../../stores';

    let friends = [];
    
    axios.post(
        PUBLIC_BACKEND_API + 'user/friends/',
        { id: $userStore.id }
    ).then((res) => {
        if (res?.data?.friends)
            friends = res.data.friends;
        console.log(friends);
    }).catch((err) => {
        console.log(err)
    });
</script>

<div>
    <div class="my-4 text-2xl text-center font-bold text-gray-700">
        Your Friends List
    </div>
    <div
        class="bg-gray-200 rounded h-full p-2 overflow-auto"
        style="height: calc(100vh - 320px)"
    >
        <ul
            tabindex="-1"
            role="listbox"
            aria-labelledby="listbox-label"
            aria-activedescendant="listbox-option-3"
        >
            {#if friends.length === 0}
                <li
                    class="
                        bg-white
                        mb-2
                        p-2
                        rounded

                        w-full
                        text-gray-900
                        relative
                        cursor-default
                        select-none
                    "
                >
                    You have no friends.
                </li>
            {:else}
                {#each friends as r}
                    <li
                        class="
                            bg-white
                            mb-2
                            p-2
                            rounded

                            w-full
                            text-gray-900
                            relative
                            flex
                            justify-between
                            cursor-pointer
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
</div>
