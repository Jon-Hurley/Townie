<script>
	import { onMount } from 'svelte';
    import { userStore } from '../../stores';
    import { getFriends } from '../../requests/friend';
	import Loading from '../../components/loading.svelte';

    let friends = [];
    let loading = true;
    
    onMount(async() => {
        friends = await getFriends($userStore.key);
        friends = [ ...friends, ...friends ]
        friends = [ ...friends, ...friends ]
        friends = [ ...friends, ...friends ]
        friends = [ ...friends, ...friends ]
        friends = [ ...friends, ...friends ]
        friends = [ ...friends, ...friends ]
        loading = false;
    });
</script>

<div style="height: 100%">
<div class="my-2 text-2xl text-center font-bold text-gray-700">
    Your Friends List
</div>

{#if loading}
    <Loading/>
{:else}
    <div
        class="
            overflow-auto
            inline-flex flex-wrap justify-center
            gap-2
            p-2
            w-full
        "
        style="max-height: 100%"
    >
        {#if friends.length}
            {#each friends as r}
                <div
                    class="
                        px-4 py-2 h-11 w-36 m-0

                        border-gray-200 border-2 rounded

                        text-gray-900 text-center
                        
                        cursor-pointer
                        hover:scale-110
                    "
                >
                    <a href={"/user/" + r.key}>
                        <!-- <img></img> -->
                        {r.username}
                    </a>
                </div>
            {/each}
        {:else}
            <div
                class="
                    px-4 py-2
                    w-full

                    border-gray-200 border-2 rounded

                    text-gray-900
                    cursor-default
                "
            >
                You have no friends.
            </div>
        {/if}
    </div>
{/if}
</div>