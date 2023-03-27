<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
	import { getUser } from '../../../requests/search';
    import Loading from '../../../general-components/loading.svelte';
	import User from './user.svelte';

    let user;

    onMount(async() => {
        const key = $page.params.slug;
        user = await getUser(key);
    });
</script>

{#if user}
    <div
        class="h-full flex flex-col"
    >
        <User
            user={user}
        />
    </div>
{:else}
    <Loading/>
{/if}