<script>
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
	import { Game } from '../../classes/Game';

	onMount(() => {
		goto('game/' + Game.getPage())
    });
</script>