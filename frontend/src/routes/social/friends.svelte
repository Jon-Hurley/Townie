<script>
	import { onMount } from 'svelte';
    import { userStore } from '../../stores';
    import { getFriends } from '../../requests/friend';

    let friends = [];
    
    onMount(async() => {
        friends = await getFriends($userStore.key);
    });
</script>

<div class="my-4 text-2xl text-center font-bold text-gray-700">
    Your Friends List
</div>

<div
    class="overflow-auto"
    style="height: 100%"
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

                    border-gray-200
                    border-2

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

                        border-gray-200
                        border-2

                        w-full
                        text-gray-900
                        relative
                        flex
                        justify-between
                        cursor-pointer
                    "
                >
                    <a href={"/user/" + r.key}>
                        <!-- <img></img> -->
                        {r.username} #{r.key}
                    </a>
                </li>
            {/each}
        {/if}
    </ul>
</div>
