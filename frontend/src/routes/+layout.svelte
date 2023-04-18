<script>
	import '../app.css';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

	import Loading from '../general-components/loading.svelte';
	import Modal from '../general-components/modal.svelte';
    import ColorLoader from './color-loader.svelte';

	import { popupQueue, userStore } from '../stores';
    import { autoLogin } from '../requests/account';

    let loaded = false;

    const redirectOnUserUpdate = (v) => {
        if (v) {
            goto('/app/game');
        } else {
            goto('/login');
        }
    };

	onMount(async () => {
        loaded = false;
        
        userStore.subscribe(redirectOnUserUpdate);

        if (!$userStore) {
            const success = await autoLogin();
        }

        loaded = true;
	});  
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

<ColorLoader/>