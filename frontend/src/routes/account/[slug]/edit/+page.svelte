<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
	import { getUser } from '../../../../requests/search';
    import Loading from '../../../../components/loading.svelte';
	import User from './edit.svelte';


    let user;

    onMount(async() => {
        user = await getUser($page.params.slug);
        user = user;
    })    
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