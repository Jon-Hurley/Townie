<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
	import { getUser } from '../../../requests/search';
    import Loading from '../../../components/loading.svelte';
	import User from './user.svelte';
	import { userStore } from '../../../stores';

    let user = $userStore;

    onMount(async() => {
        user = $userStore;
        user.purchases = [
            {
                name: "PP Music",
                badge: "M9 9l10.5-3m0 6.553v3.75a2.25 2.25 0 01-1.632 2.163l-1.32.377a1.803 1.803 0 11-.99-3.467l2.31-.66a2.25 2.25 0 001.632-2.163zm0 0V2.25L9 5.25v10.303m0 0v3.75a2.25 2.25 0 01-1.632 2.163l-1.32.377a1.803 1.803 0 01-.99-3.467l2.31-.66A2.25 2.25 0 009 15.553z"
            }
        ]
        user.purchases = [ ...user.purchases, ...user.purchases ]
        user.purchases = [ ...user.purchases, ...user.purchases ]
        user.purchases = [ ...user.purchases, ...user.purchases ]
        user.purchases = [ ...user.purchases, ...user.purchases ]
        user = user;
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