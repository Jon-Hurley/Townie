<script>
	import { onMount } from 'svelte';

	import Navbar from '../app/navbar.svelte';
	import AccountBar from '../app/account-bar.svelte';
	import Loading from '../../general-components/loading.svelte';
	import Audio from './audio.svelte';
	import { page } from '$app/stores';

	import { handlePurchaseUpdates, userStore } from '../../stores';

	onMount(() => {
		userStore.subscribe((user) => {
			if (user?.token) {
				sessionStorage.setItem('token', user.token);
			}
			handlePurchaseUpdates(user);
		});
	});
</script>

{#if $userStore}
	<AccountBar />
	<div
		class="m-0 p-4"
		style="
            height: calc(100vh - 120px);
            max-height: calc(100vh - 120px);
            width: 100vw;
            overflow-y: auto;
        "
	>
		<slot />
	</div>
	<Navbar />
{:else}
	<Loading />
{/if}

<Audio />
