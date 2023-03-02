<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
	import { getUser } from '../../../requests/search';
    import Loading from '../../../components/loading.svelte';
	import User from './edit/updateAccount.svelte';
	import { userStore } from '../../../stores';


    let user = $userStore;

    onMount(async() => {
        user = userStore
    })    
</script>

{#if user}
    <div
        class="h-full flex flex-col"
    >
        <User
            user={$userStore}
        />
    </div>
{:else}
    <Loading/>
{/if}