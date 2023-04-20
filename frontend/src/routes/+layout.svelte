<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import Loading from '../general-components/loading.svelte';
	import Modal from '../general-components/modal.svelte';
	import ColorLoader from './color-loader.svelte';

	import { popupQueue, userStore } from '../stores';
	import { autoLogin } from '../requests/account';

	let loaded = false;
	let prevUser = null;

	$: console.log($page);

	const redirectOnUserUpdate = (v) => {
		if (v) {
			if (!prevUser) {
				const lastPage = localStorage.getItem('lastPage');
				if (lastPage) {
					goto(lastPage);
				} else {
					goto('/app/game');
				}
			}
		} else {
			goto('/login');
		}
		prevUser = v;
	};

	onMount(async () => {
		loaded = false;

		page.subscribe((page) => {
			if (page?.route?.id?.includes('app')) {
				let url = page.url.href;
				localStorage.setItem('lastPage', url);
			}
		});

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
		<slot />
	</div>
{:else}
	<Loading />
{/if}

{#if $popupQueue.length}
	<Modal {...$popupQueue[0]} />
{/if}

<ColorLoader />
