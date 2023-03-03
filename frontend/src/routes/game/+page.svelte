<script>
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
	import { gameStore } from '../../stores';

	onMount(() => {
		goto(`/game/${$gameStore?.game?.page || 'join'}`)
    });
</script>