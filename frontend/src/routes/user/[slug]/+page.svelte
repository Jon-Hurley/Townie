<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
	import { getUser } from '../../../requests/search';
    import Loading from '../../../general-components/loading.svelte';
	import User from './user.svelte';

    let user;

    const loadUser = async() => {
        const key = $page.params.slug;
        user = await getUser(key);
    }

    onMount(loadUser);
</script>

{#if user}
    <div
        class="h-full flex flex-col"
    >
        <User
            user={user}
            reloadUser={loadUser}
        />
    </div>
{:else}
    <Loading/>
{/if}