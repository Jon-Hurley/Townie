<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    import Navbar from '../app/navbar.svelte';
    import AccountBar from '../app/account-bar.svelte';
	import Loading from '../../general-components/loading.svelte';
  
	import { userStore } from '../../stores';

	onMount(() => {
        userStore.subscribe(user => {
            if (user?.token) {
                sessionStorage.setItem('token', user.token);
            }
        });
	});

    $: if (!$userStore) goto('/login');
</script>

{#if $userStore}
    <AccountBar/>
    <div
        class="m-0 p-4"
        style="
            height: calc(100vh - 120px);
            max-height: calc(100vh - 120px);
            width: 100vw;
        "
    >
        <slot/>
    </div>
    <Navbar/>
{:else}
    <Loading/>
{/if}