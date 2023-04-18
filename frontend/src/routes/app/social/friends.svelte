<script>
	import { onMount } from 'svelte';

    import Loading from '../../../general-components/loading.svelte';
    
    import { userStore } from '../../../stores';
    import { getFriends } from '../../../requests/friend';
	import { gridItem, hr, largeTitle, listItem } from '../../../css';
	import Username from '../../../general-components/username.svelte';

    let friends = [];
    let loading = true;
    
    onMount(async() => {
        if (!$userStore) return;
        friends = await getFriends($userStore.key);
        loading = false;
    });
</script>

<div class="{largeTitle}">
    Your Friends List
</div>
<hr class="{hr}"/>

{#if loading}
    <Loading/>
{:else}
    <div
        class="
            inline-flex flex-wrap justify-center
            gap-2
            w-full
        "
        style="max-height: 100%"
    >
        {#if friends.length}
            {#each friends as r}
                <div class="{gridItem}">
                    <a href={"/app/user/" + r.key}>
                        <Username user={r}/>
                    </a>
                </div>
            {/each}
        {:else}
            <div
                class="{listItem}"
            >
                You have no friends.
            </div>
        {/if}
    </div>
{/if}