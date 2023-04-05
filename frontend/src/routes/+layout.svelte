<script>
	import '../app.css';

    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';

	import Loading from '../general-components/loading.svelte';
	import Modal from '../general-components/modal.svelte';
    
	import { popupQueue, userStore } from '../stores';
    import { autoLogin } from '../requests/account';
    $: console.log('NEW USER: ', $userStore);

    let loaded = false;
	onMount(async () => {
        loaded = false;
        if (!$userStore) {
            const res = await autoLogin();
            if (!res) {
                goto('/login');
            }
        }
        loaded = true;
	});

	let prevUser = false;
	$: {
        if (!prevUser && $userStore) {
            console.log($page?.route?.id)
            if ($page?.route?.id && !$page.route.id.includes('app')) {
                goto('/app/game');
            }
        }
		prevUser = $userStore;
	}
</script>

{#if loaded}
    <div
        class="
            flex flex-col justify-between items-center
            h-screen w-screen max-h-screen max-w-screen
        "
    >
        <slot/>
    </div>
{:else}
    <Loading/>
{/if}

{#if $popupQueue.length}
    <Modal
        {...$popupQueue[0]}
    />
{/if}