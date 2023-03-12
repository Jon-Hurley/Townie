<script>
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
	import { Game } from '../../stores';

	onMount(() => {
		goto('game/' + Game.getPage())
    });
</script>