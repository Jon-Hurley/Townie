<script>
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
	import { Game } from '../../Game';

	onMount(() => {
		goto('game/' + Game.getPage())
    });
</script>